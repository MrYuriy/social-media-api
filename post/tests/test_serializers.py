from django.contrib.auth import get_user_model
from django.test import TestCase

from post.models import Hashtag, Post
from post.serializers import (
    HashtagSerializer,
    HashtagsSerializer,
    PostSerializer,
    PostDetailSerializer,
)


class HashtagSerializerTest(TestCase):
    def test_valid_data(self):
        serializer = HashtagSerializer(data={"name": "test hashtag"})
        self.assertTrue(serializer.is_valid())

    def test_missing_name(self):
        serializer = HashtagSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_unique_name(self):
        Hashtag.objects.create(name="existing hashtag")
        serializer = HashtagSerializer(data={"name": "existing hashtag"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class HashtagsSerializerTest(TestCase):
    def test_valid_data(self):
        data = [{"name": "hashtag1"}, {"name": "hashtag2"}]
        serializer = HashtagsSerializer(data=data, many=True)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = [{"name": "hashtag1"}, {"name": ""}]
        serializer = HashtagsSerializer(data=data, many=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors[1])


class PostSerializerTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(
            email="testuser@gmail.com", password="testpassword"
        )

    def test_valid_data(self):
        data = {"author": self.user.id, "title": "Test Post", "content": "Test content"}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_fields(self):
        data = {"author": self.user.id, "title": "Test Post"}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("content", serializer.errors)

    def test_read_only_fields(self):
        post = Post.objects.create(
            author=self.user, title="Test Post", content="Test content"
        )
        data = {
            "id": post.id,
            "author": self.user.id,
            "title": "Updated Post",
            "content": "Updated content",
        }
        serializer = PostSerializer(instance=post, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.save().author == self.user)


class PostDetailSerializerTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="testpassword"
        )

    def test_hashtag_serializer(self):
        hashtag = Hashtag.objects.create(name="test hashtag")
        post = Post.objects.create(
            author=self.user, title="Test Post", content="Test content"
        )
        post.hashtag.add(hashtag)

        serializer = PostDetailSerializer(instance=post)
        self.assertIn("hashtag", serializer.data)
        self.assertEqual(serializer.data["hashtag"], [hashtag.name])

    def test_read_only_fields(self):
        post = Post.objects.create(
            author=self.user, title="Test Post", content="Test content"
        )
        data = {
            "id": post.id,
            "author": self.user.id,
            "title": "Updated Post",
            "content": "Updated content",
        }
        serializer = PostDetailSerializer(instance=post, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.save().author == self.user)
