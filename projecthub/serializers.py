from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from projecthub.models import Project, Issue, Comment, Contribute


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]


class ProjectDetailSerializer(ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    issues = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "name", "description", "author", "type", "created_time", "issues", "contributors"]
        read_only_fields = ["id", "author", "issues", "contributors"]

    def get_issues(self, project):
        issues = Issue.objects.filter(project=project)
        return IssueListSerializer(issues, many=True).data

    def get_contributors(self, project):
        """import différé pour éviter l'importation circulaire"""
        from authentication.serializers import UserListSerializer
        contributors = project.contributors.all()
        return UserListSerializer([contrib.author for contrib in contributors], many=True).data


class IssueListSerializer(ModelSerializer):
    project_name = serializers.CharField(source="project.name")

    class Meta:
        model = Issue
        fields = ["id", "name", "project_name"]


class IssueDetailSerializer(ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    comments = serializers.SerializerMethodField()
    assigned_contributor = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ["id", "name", "description", "author", "project", "project_name", "priority", "type", "status",
                  "created_time", "comments", "assigned_contributor"]
        read_only_fields = ["id", "author", "project_name", "comments"]

    def get_comments(self, issue):
        comments = Comment.objects.filter(issue=issue)
        return CommentListSerializer(comments, many=True).data

    def get_assigned_contributor(self, issue):
        """import différé pour éviter l'importation circulaire"""
        from authentication.serializers import UserListSerializer
        if issue.assigned_contributor:
            return UserListSerializer(issue.assigned_contributor).data
        return None


class CommentListSerializer(ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    issue_name = serializers.CharField(source="issue.name", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "issue", "issue_name"]


class CommentDetailSerializer(ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    issue_name = serializers.CharField(source="issue.name", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue", "issue_name", "created_time"]
        read_only_fields = ["id", "author", "issue_name"]


class ContributeSerializer(ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Contribute
        fields = ["id", "author", "author_name", "project", "project_name", "created_time"]
        read_only_fields = ["id", "author_name", "project_name"]
