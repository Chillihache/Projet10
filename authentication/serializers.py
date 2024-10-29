from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from authentication.models import User
from projecthub.models import Project, Issue
from projecthub.serializers import ProjectListSerializer, IssueListSerializer


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserDetailSerializer(ModelSerializer):
    contributions = SerializerMethodField()
    assigned_issues = SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "password", "age", "can_be_contacted", "can_data_be_shared", "created_time",
                  "contributions", "assigned_issues"]
        read_only_fields = ["id", "contributions", "assigned_issues"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_age(self, value):
        if value and value < 15:
            raise ValidationError("Vous devez avoir au minimum 15 ans pour vous inscrire")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            age=validated_data["age"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"]
        )
        return user

    def get_contributions(self, user):
        contributions = Project.objects.filter(contributors__author=user)
        return ProjectListSerializer(contributions, many=True).data

    def get_assigned_issues(self, user):
        assigned_issues = Issue.objects.filter(assigned_contributor=user)
        return IssueListSerializer(assigned_issues, many=True).data


