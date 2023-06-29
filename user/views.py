from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.models import Profile, User
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
            queryset = queryset.filter(email__icontains=email)

        if username:
            queryset = queryset.filter(username__incontains=username)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileListSerializer

    @action(detail=True, methods=["post"])
    def follow_switch(self, request, pk=None):
        profile = Profile.objects.get(user=request.user)

        if Profile.objects.filter(followers__id=pk).exists():
            profile.following.remove(User.objects.get(pk=pk))
            request.user.profile.followers.remove(profile.user)
            return Response({"status": "unfollow"})
        profile.following.add(User.objects.get(pk=pk))
        request.user.profile.followers.add(profile.user)
        return Response({"status": "follow"})
