from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication import models


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    class Meta:
        model = models.User
        fields = (
            "username",
            "email",
            "password",
        )

    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters."
            )

        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = models.User
        fields = ("token",)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, write_only=True, style={"input_type": "password"}
    )
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = models.User
        fields = (
            "email",
            "password",
            "username",
            "tokens",
        )

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(
            email=email,
            password=password,
        )

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again.")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin.")

        if not user.is_verified:
            raise AuthenticationFailed("Account is not verified.")

        return {"email": user.email, "username": user.username, "tokens": user.tokens}
