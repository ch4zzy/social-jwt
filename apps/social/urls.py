from django.urls import path, include
from rest_framework import routers

from apps.social.views import PostViewSet, UserViewSet, PostActionAPIView, AnalyticsViewSet, UserActivityViewSet

app_name = "api_social"

router = routers.DefaultRouter()
router.register(r"post", PostViewSet)
router.register(r"user", UserViewSet)
router.register(r"analytics", AnalyticsViewSet, basename="analytics")
router.register(r"activity", UserActivityViewSet, basename="activity")

urlpatterns = [
    path("action/<int:pk>/", PostActionAPIView.as_view(), name="post-action"),
    path("", include(router.urls)),
]
