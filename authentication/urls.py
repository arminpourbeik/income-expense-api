from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from authentication import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="email-verify"),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
    path(
        "request-rest-email/",
        views.RequestPasswordResetEmail.as_view(),
        name="request-rest-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        views.PasswordTokenCheckApi.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        views.SetNewPasswordApiView.as_view(),
        name="password-reset-complete",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]