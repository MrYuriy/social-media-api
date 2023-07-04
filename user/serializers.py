from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class FollowsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email",)
        list_serializer_class = serializers.ListSerializer

    def to_representation(self, instance):
        return instance.email


class ProfileListSerializer(serializers.ModelSerializer):
    followers = FollowsSerializer(read_only=True, many=True)
    following = FollowsSerializer(read_only=True, many=True)
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "username",
            "bio",
            "image",
            "followers",
            "following",
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    followers = FollowsSerializer(read_only=True, many=True)
    following = FollowsSerializer(read_only=True, many=True)
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "email",
            "username",
            "image",
            "followers",
            "following",
        )
