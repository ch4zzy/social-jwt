from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.social.models import Post
from apps.social.serializers import (
    PostActionSerializer,
    PostAnalyticsSerializer,
    PostSerializer,
    UserSerializer,
)
from apps.social.validators import (
    validate_date,
    validate_existing_like,
    validate_unique_like,
)


class PostViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @action(detail=True, methods=["get"])
    def user_list(self, request, pk):
        """
        Returns a list of posts for current user.
        GET: ~/api/post/
        GET: ~/api/post/{pk}/ - detail post
        """

        owner = get_object_or_404(User, id=pk)
        queryset = self.get_queryset().filter(owner=owner)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class PostActionAPIView(generics.CreateAPIView, mixins.CreateModelMixin):
    serializer_class = PostActionSerializer

    def create(self, request, *args, **kwargs):
        """
        Create action: like or unlike.
        POST: ~/api/action/{pk}/
        """

        user = request.user
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action_type = request.data.get("action_type")

        if action_type == "like":
            validate_unique_like(user, post)
            post.user_likes.add(user)
            post.total_likes += 1
        elif action_type == "unlike":
            validate_existing_like(user, post)
            post.user_likes.remove(user)
            post.total_likes -= 1
        else:
            return Response({"error": "Invalid action type"}, status=status.HTTP_400_BAD_REQUEST)

        post.save()
        serializer = PostActionSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnalyticsViewSet(viewsets.ViewSet, mixins.ListModelMixin):
    serializer_class = PostAnalyticsSerializer

    def list(self, request):
        """
        Show list of some analytics.
        GET: ~/api/analitics/?date_from****-**-**&date_to****-**-**/
        """

        serializer = PostAnalyticsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        date_from = serializer.validated_data.get("date_from")
        date_to = serializer.validated_data.get("date_to")

        start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
        end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
        validate_date(start_date, end_date)

        if start_date and end_date:
            analytics = Post.objects.filter(updated__date__range=(start_date, end_date)).aggregate(
                total_likes=Sum("total_likes")
            )
            return Response(analytics)
        return Response([])


class UserActivityViewSet(viewsets.ViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Show list with user activity.
        GET: ~/api/activity/
        """

        user = self.request.user
        user.last_request = timezone.now()
        user.save()
        activity_data = {
            "last_login": user.last_login,
            "last_request": user.last_request,
        }
        return Response(activity_data)


class UserViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
