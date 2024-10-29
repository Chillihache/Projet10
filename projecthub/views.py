from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework import status

from projecthub.models import Project, Issue, Comment, Contribute
from projecthub.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                    IssueListSerializer, IssueDetailSerializer,
                                    CommentListSerializer, CommentDetailSerializer,
                                    ContributeSerializer)


class DestroyUpdatePermissionsMixin:
    def check_object_permissions(self, request, obj):
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("Not allowed")

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_permissions(obj)
        return super().update(request, *args, **kwargs)


class ProjectViewSet(DestroyUpdatePermissionsMixin, ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(contributors__author=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssueViewSet(DestroyUpdatePermissionsMixin, ModelViewSet):
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        projects = Project.objects.filter(contributors__author=self.request.user)
        return Issue.objects.filter(project__in=projects)

    def get_serializer_class(self):
        if self.action == "list":
            return IssueListSerializer
        return IssueDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = request.data.get("project")
        assigned_contributor_id = request.data.get("assigned_contributor")

        try:
            project = Project.objects.get(id=project_id)  # Obtenez le projet
        except Project.DoesNotExist:
            raise ValidationError("The project does not exist.")

        if assigned_contributor_id:
            if not project.contributors.filter(author_id=assigned_contributor_id).exists():
                raise ValidationError("The assigned contributor must be a contributor on the project")

        serializer.save(author=request.user, assigned_contributor_id=assigned_contributor_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = self.get_serializer(issue, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        project = issue.project
        assigned_contributor_id = request.data.get("assigned_contributor")

        if assigned_contributor_id:
            if not project.contributors.filter(author_id=assigned_contributor_id).exists():
                raise ValidationError("The assigned contributor must be a contributor on the project")

        # Sauvegarde des modifications
        serializer.save(assigned_contributor_id=assigned_contributor_id)  # Assurez-vous que le champ soit mis à jour
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(DestroyUpdatePermissionsMixin, ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        projects = Project.objects.filter(contributors__author=self.request.user)
        issues = Issue.objects.filter(project__in=projects)
        return Comment.objects.filter(issue__in=issues)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        return CommentDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContributeViewSet(ModelViewSet):
    queryset = Contribute.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return ContributeSerializer




