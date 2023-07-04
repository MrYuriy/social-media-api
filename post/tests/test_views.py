from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from post.models import Hashtag, Post
from post.serializers import HashtagSerializer, PostSerializer, PostDetailSerializer
from django.contrib.auth import get_user_model
from user.models import Profile

User = get_user_model()


class HashtagViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hashtag1 = Hashtag.objects.create(name="test1")
        self.hashtag2 = Hashtag.objects.create(name="test2")

    def test_list_hashtags(self):
        response = self.client.get(reverse("post:hashtag-list"))
        hashtags = Hashtag.objects.all()
        serializer = HashtagSerializer(hashtags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_hashtag(self):
        data = {
            'name': 'new_hashtag'
        }
        response = self.client.post(reverse("post:hashtag-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hashtag.objects.count(), 3)
        self.assertEqual(Hashtag.objects.last().name, 'new_hashtag')

    def test_retrieve_hashtag(self):
        response = self.client.get(reverse("post:hashtag-detail", kwargs={"pk": self.hashtag1.id}))
        hashtag = Hashtag.objects.get(id=self.hashtag1.id)
        serializer = HashtagSerializer(hashtag)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_hashtag(self):
        data = {
            'name': 'updated_hashtag'
        }
        response = self.client.put(reverse("post:hashtag-detail", kwargs={"pk": self.hashtag1.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Hashtag.objects.get(id=self.hashtag1.id).name, 'updated_hashtag')

    def test_delete_hashtag(self):
        response = self.client.delete(reverse("post:hashtag-detail", kwargs={"pk": self.hashtag1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hashtag.objects.filter(id=self.hashtag1.id).exists())


class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@email.com', password='testpass')
        self.profile = Profile.objects.create(
            user=self.user,
            username="testuser",
            bio="Test bio",
        )
        self.client.force_authenticate(user=self.user)
        self.hashtag1 = Hashtag.objects.create(name="test1")
        self.hashtag2 = Hashtag.objects.create(name="test2")
        self.post1 = Post.objects.create(author=self.user, title="Test Post 1", content="Test content 1")
        self.post1.hashtag.add(self.hashtag1)
        self.post2 = Post.objects.create(author=self.user, title="Test Post 2", content="Test content 2")
        self.post2.hashtag.add(self.hashtag2)

    def test_list_posts(self):
        response = self.client.get(reverse("post:post-list"))
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_post(self):
        data = {
            'title': 'New Post',
            'content': 'New post content',
            'hashtag': [self.hashtag1.id, self.hashtag2.id],
            "author": self.user.id
        }

        response = self.client.post(reverse("post:post-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.last().title, 'New Post')
        self.assertEqual(list(Post.objects.last().hashtag.all()), [self.hashtag1, self.hashtag2])

    def test_retrieve_post(self):
        response = self.client.get(reverse("post:post-detail", kwargs={"pk": self.post1.id}))
        post = Post.objects.get(id=self.post1.id)
        serializer = PostDetailSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_post(self):
        data = {
            'title': 'Updated Post',
            'content': 'Updated post content',
            'hashtag': [self.hashtag1.id],
            "author": self.user.id
        }
        response = self.client.put(reverse("post:post-detail", kwargs={"pk": self.post1.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post1.id).title, 'Updated Post')
        self.assertEqual(list(Post.objects.get(id=self.post1.id).hashtag.all()), [self.hashtag1])

    def test_delete_post(self):
        response = self.client.delete(reverse("post:post-detail", kwargs={"pk": self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
