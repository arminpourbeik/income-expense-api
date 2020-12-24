from django.contrib import auth
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import TokenError

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

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
    # tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = models.User.objects.get(email=obj["email"])

        return {
            "access": user.tokens["access"],
            "refresh": user.tokens["refresh"],
        }

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


class RequestPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ("email",)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = (
            "password",
            "token",
            "uidb64",
        )

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user

        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError as e:
            self.fail("bad_token")
