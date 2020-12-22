import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.utils.encoding import (
    smart_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from rest_framework import generics, views
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authentication import serializers
from authentication.models import User
from authentication.utils import Util
from authentication.renderers import UserRenderer


class RegistrationView(generics.GenericAPIView):
    """
    View for user registration
    """

    serializer_class = serializers.RegistrationSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user=user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        abs_url = f"http://{current_site}{relative_link}?token={str(token)}"
        email_body = (
            f"Hi {user.username} use the link below to verify your email \n {abs_url}"
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data=data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    """
    View for confirm email with token
    """

    serializer_class = serializers.EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, config("SECRET_KEY"))
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {
                    "email": "Successfully activated",
                },
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "error": "Activation link expired",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.DecodeError:
            return Response(
                {
                    "error": "Invalid token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginApiView(generics.GenericAPIView):
    """
    View for login user
    """

    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    """
    View for requesting password-reset Email
    """

    serializer_class = serializers.RequestPasswordEmailRequestSerializer

    def post(self, request):
        data = {"request": request, "data": request.data}
        serializer = self.serializer_class(data=request.data)

        email = request.data["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # We want to sent user_id but encoded
            uid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                "password-reset-confirm", kwargs={"uidb64": uid64, "token": token}
            )
            abs_url = f"http://{current_site}{relative_link}"
            email_body = f"Hi, use the link below to reset your password \n {abs_url}"
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }

            Util.send_email(data)

        return Response(
            {"success": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckApi(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response(
                    {"error": "Token is not valid, please request a new one."},
                    status=status.status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    "success": True,
                    "message": "Credentials is valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )

        except DjangoUnicodeDecodeError:
            return Response(
                {"error": "Token is not valid, please request a new one."},
                status=status.status.HTTP_401_UNAUTHORIZED,
            )


class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = serializers.SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )
