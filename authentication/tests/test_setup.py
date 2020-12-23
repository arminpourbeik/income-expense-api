from rest_framework.test import APITestCase
from django.urls import reverse

from faker import Faker


class TestSetup(APITestCase):
    fake = Faker()

    user_data = {
        "email": fake.email(),
        "username": fake.email().split("@")[0],
        "password": "p@assw0rd",
    }

    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def tearDown(self) -> None:
        return super().tearDown()
