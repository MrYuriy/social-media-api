from rest_framework import serializers

from .models import Hashtag, Post


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("name",)


class HashtagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("name",)
        list_serializer_class = serializers.ListSerializer

    def to_representation(self, instance):
        return instance.name


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "content",
            "hashtag",
        )
        read_only_fields = ("user",)


class PostDetailSerializer(serializers.ModelSerializer):
    hashtag = HashtagsSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("user",)
