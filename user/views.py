from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.models import Profile
from user.permissions import IsOwnerOrReadOnly
from user.serializers import (
    UserSerializer,
    ProfileListSerializer,
    ProfileDetailSerializer,
)


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LogoutUserView(APIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        request.usern.auth_toke.delete()
        return Response(status=status.HTTP_200_OK)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        email = self.request.query_params.get("email")
        username = self.request.query_params.get("username")

        if email:
            queryset = queryset.filter(email__contains=email)

        if username:
            queryset = queryset.filter(username__contains=username)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileListSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=str,
                description="Filtering by username (write some symbol that "
                            "contains in username). ex. ?username=yurii",
            ),
            OpenApiParameter(
                "bio",
                type=str,
                description="Filtering by bio (write some symbol that "
                            "contains in bio). ex. ?bio=bio",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def follow_switch(self, request, pk=None):
        profile = Profile.objects.get(user=request.user)
        user = request.user

        if profile.followers.filter(pk=user.pk).exists():
            profile.followers.remove(user)
            user.profile.following.remove(profile.user)
            return Response({"status": "unfollow"})
        profile.followers.add(user)
        user.profile.following.add(profile.user)
        return Response({"status": "follow"})
