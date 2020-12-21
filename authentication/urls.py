from django.urls import path

from authentication import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="email-verify"),
    path("login/", views.LoginApiView.as_view(), name="login"),
]