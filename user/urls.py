
from django.urls import path

from user.views import (
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    LogoutUserView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
