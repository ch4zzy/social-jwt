from django.contrib.auth.models import User
from rest_framework import serializers

from apps.social.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "created",
            "updated",
            "total_likes",
        )


class PostActionSerializer(serializers.ModelSerializer):
    """
    Serializer for performing actions on the Post model.
    """

    class Meta:
        model = Post
        fields = (
            "id",
            "created",
            "updated",
            "total_likes",
        )


class PostAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for the post analytics.
    """

    date_from = serializers.DateField()
    date_to = serializers.DateField()

    class Meta:
        model = Post
        fields = ("id", "updated", "total_likes", "date_from", "date_to")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("owner", None)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
