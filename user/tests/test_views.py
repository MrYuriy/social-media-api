from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from user.models import Profile

User = get_user_model()


class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_create_user_success(self):
        response = self.client.post(
            reverse("user:create"),
            self.user_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")

    def test_create_user_invalid_data(self):
        invalid_user_data = {
            "email": "invalidemail",
            "password": "testpassword",
        }
        response = self.client.post(
            reverse("user:create"),
            invalid_user_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class ManageUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_retrieve_user(self):
        response = self.client.get(reverse("user:manage"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_update_user(self):
        updated_user_data = {
            "email": "updated@example.com",
            "password": "updatedpassword",
        }
        response = self.client.patch(reverse("user:manage"), updated_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, "updated@example.com")


class ProfileViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.profile = Profile.objects.create(
            user=self.user,
            username="testuser",
            bio="Test bio",
        )

    def test_list_profiles(self):
        response = self.client.get(reverse("user:profile-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], "test@example.com")

    def test_retrieve_profile(self):
        response = self.client.get(reverse("user:profile-detail", args=[self.profile.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "test@example.com")

    def test_filter_profiles_by_username(self):
        response = self.client.get(reverse("user:profile-list"), {"username": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], "test@example.com")

    def test_filter_profiles_by_bio(self):
        response = self.client.get(reverse("user:profile-list"), {"bio": "bio"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], "test@example.com")

