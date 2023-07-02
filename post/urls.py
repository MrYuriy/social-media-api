from django.urls import path, include
from rest_framework import routers
from .views import HashtagViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r"hashtag", HashtagViewSet, basename="hashtag")
router.register(r"post", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "post"
