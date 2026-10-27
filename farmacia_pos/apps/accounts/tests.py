from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import User


class UserModelTests(TestCase):
    def test_custom_user_is_active_model(self):
        self.assertIs(get_user_model(), User)

    def test_create_user_hashes_password(self):
        user = User.objects.create_user(username="cajero.demo", password="clave-ficticia-123")
        self.assertTrue(user.is_active)
        self.assertNotEqual(user.password, "clave-ficticia-123")
        self.assertTrue(user.check_password("clave-ficticia-123"))
