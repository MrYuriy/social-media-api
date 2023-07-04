from django.test import TestCase
from django.contrib.auth import get_user_model
from post.models import Hashtag, Post


class HashtagModelTest(TestCase):
    def setUp(self):
        self.hashtag = Hashtag.objects.create(name="test hashtag")

    def test_name_field(self):
        field_label = self.hashtag._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        max_length = self.hashtag._meta.get_field("name").max_length
        self.assertEquals(max_length, 120)

    def test_name_unique(self):
        unique = self.hashtag._meta.get_field("name").unique
        self.assertTrue(unique)

    def test_str_representation(self):
        self.assertEquals(str(self.hashtag), self.hashtag.name)


class PostModelTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(email="testuser@mail.com", password="testpassword")
        self.post = Post.objects.create(author=self.user, title="Test Post", content="Test content")

    def test_author_field(self):
        field_label = self.post._meta.get_field("author").verbose_name
        self.assertEquals(field_label, "author")

    def test_title_field(self):
        field_label = self.post._meta.get_field("title").verbose_name
        self.assertEquals(field_label, "title")

    def test_title_max_length(self):
        max_length = self.post._meta.get_field("title").max_length
        self.assertEquals(max_length, 255)

    def test_content_field(self):
        field_label = self.post._meta.get_field("content").verbose_name
        self.assertEquals(field_label, "content")

    def test_created_field(self):
        field_label = self.post._meta.get_field("created").verbose_name
        self.assertEquals(field_label, "created")

    def test_hashtag_field(self):
        field_label = self.post._meta.get_field("hashtag").verbose_name
        self.assertEquals(field_label, "hashtag")

    def test_author_relationship(self):
        related_name = self.post._meta.get_field("author").related_query_name()
        self.assertEquals(related_name, "author")

    def test_hashtag_relationship(self):
        related_name = self.post._meta.get_field("hashtag").related_query_name()
        self.assertEquals(related_name, "post")

    def test_str_representation(self):
        self.assertEquals(str(self.post), self.post.title)
