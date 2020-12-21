from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics, views
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authentication import serializers
from authentication.models import User
from authentication.utils import Util


class RegistrationView(generics.GenericAPIView):
    """
    View for user registration
    """

    serializer_class = serializers.RegistrationSerializer

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
