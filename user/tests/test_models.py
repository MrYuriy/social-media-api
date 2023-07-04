from django.test import TestCase
from django.contrib.auth import get_user_model

from user.models import Profile

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("adminpassword"))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            username="testuser",
            bio="Test bio",
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.username, "testuser")
        self.assertEqual(self.profile.bio, "Test bio")

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "test@example.com profile")