from rest_framework import serializers
from app.models.user import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    full_name = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'phone',
            'avatar',
            'avatar_url'
        ]
