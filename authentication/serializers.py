from rest_framework.serializers import ModelSerializer, ValidationError
from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "age", "can_be_contacted", "can_data_be_shared", "created_time"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_age(self, value):
        if value is not None and value < 15:
            raise ValidationError("Vous devez avoir au minimum 15 ans pour vous inscrire")
        return value

    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            age=validated_data["age"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"]
        )
        return user