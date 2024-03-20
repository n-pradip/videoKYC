from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "profile_pic",
            "branch_name",
            "branch_code",
            "department",
            "functional_title",
        )
