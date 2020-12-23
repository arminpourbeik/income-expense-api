from .test_setup import TestSetup

from authentication.models import User


class TestViews(TestSetup):
    def test_user_cannot_register_with_no_data(self):
        """
        Make sure user cannot register via empty email, username, and password
        """
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_with_correct_data(self):
        """
        Make sure user can register via empty email, username, and password
        """
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 201)

        self.assertEqual(res.data["email"], self.user_data["email"])
        self.assertEqual(res.data["username"], self.user_data["username"])

    def test_user_cannot_login_with_unverified_email(self):
        """
        Make sure that an unverified user cannot login
        """
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")

        self.assertEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        """
        Make sure that a verified user can login
        """
        register_res = self.client.post(
            self.register_url, self.user_data, format="json"
        )

        # Confrim user by email
        email = register_res.data["email"]
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()

        res = self.client.post(self.login_url, self.user_data, format="json")

        self.assertEqual(res.status_code, 200)
