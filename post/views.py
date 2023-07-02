from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .permissions import IsOwnerOrReadOnly
from .serializers import HashtagSerializer, PostSerializer, PostDetailSerializer
from .models import Hashtag, Post


class HashtagViewSet(ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    authentication_classes = TokenAuthentication
    permission_classes = IsAuthenticated


class PostViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        following = self.request.user.profile.following.all()
        queryset = self.queryset.filter(
            Q(author__in=list(following)) | Q(author=self.request.user)
        )
        author = self.request.query_params.get("author")
        hashtag = self.request.query_params.get("hashtag")

        if author:
            queryset = queryset.filter(author__in=author)

        if hashtag:
            queryset = queryset.filter(hashtag__name__icontains=hashtag)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "author",
                type=int,
                description="Filtering posts by user id ex. ?author=1",
            ),
            OpenApiParameter(
                "hashtag",
                type=str,
                description="Filtering by hashtag (write some symbol that "
                            "contains in username). ex. ?hashtag=po",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
