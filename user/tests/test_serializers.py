from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import Profile
from user.serializers import UserSerializer, ProfileListSerializer, ProfileDetailSerializer, FollowsSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "is_staff": False,
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword"))
        self.assertFalse(user.is_staff)

    def test_update_user(self):
        user = User.objects.create_user(**self.user_data)
        updated_user_data = {
            "email": "updated@example.com",
            "password": "updatedpassword",
            "is_staff": True,
        }
        serializer = UserSerializer(instance=user, data=updated_user_data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        self.assertEqual(updated_user.email, "updated@example.com")
        self.assertTrue(updated_user.check_password("updatedpassword"))
        self.assertFalse(updated_user.is_staff)

    def test_update_user_password(self):
        user = User.objects.create_user(**self.user_data)
        updated_user_data = {
            "email": "test@example.com",
            "password": "updatedpassword",
            "is_staff": True,
        }
        serializer = UserSerializer(instance=user, data=updated_user_data)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password("updatedpassword"))


class FollowsSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        self.another_user = User.objects.create_user(
            email="another@example.com",
            password="anotherpassword",
        )
        self.followers = [self.user, self.another_user]

    def test_representation(self):
        serializer = FollowsSerializer(instance=self.followers, many=True)
        expected_data = [
            "test@example.com",
            "another@example.com"
        ]
        self.assertEqual(serializer.data, expected_data)


class ProfileListSerializerTest(TestCase):
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

    def test_representation(self):
        serializer = ProfileListSerializer(instance=self.profile)
        expected_data = {
            "id": 1,
            "user": "test@example.com",
            "username": "testuser",
            "bio": "Test bio",
            "image": None,
            "followers": [],
            "following": [],
        }
        self.assertEqual(serializer.data, expected_data)


class ProfileDetailSerializerTest(TestCase):
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

    def test_representation(self):
        serializer = ProfileDetailSerializer(instance=self.profile)
        expected_data = {
            "id": self.profile.id,
            "user": "test@example.com",
            "email": "test@example.com",
            "username": "testuser",
            "image": None,
            "followers": [],
            "following": [],
        }
        self.assertEqual(serializer.data, expected_data)
