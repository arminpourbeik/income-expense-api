from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request):
        pass
