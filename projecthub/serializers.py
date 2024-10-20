from rest_framework.serializers import ModelSerializer
from projecthub.models import Project, Issue, Comment, Contribute


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "author", "type"]
        read_only_fields = ["id", "author"]

