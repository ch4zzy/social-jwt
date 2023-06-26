from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """
    Model representing a user's post with ownership, timestamps, and user likes.
    """
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
    )
    total_likes = models.IntegerField(db_index=True, default=0, blank=True)
