from rest_framework import routers

from django.urls import path, include

from user.views import (
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    LogoutUserView,
    ProfileViewSet,
)

router = routers.DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("", include(router.urls)),
]

app_name = "user"
