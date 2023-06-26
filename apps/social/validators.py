from rest_framework.exceptions import ValidationError
from django.conf import settings
from datetime import datetime
from rest_framework import status

def validate_unique_like(user, post):
    """
    Check if the user has already liked the post.
    """

    if user in post.user_likes.all():
        if settings.DEBUG:
            raise ValidationError("You have already liked this post.")


def validate_existing_like(user, post):
    """
    Check if the user has not liked the post.
    """

    if user not in post.user_likes.all():
        if settings.DEBUG:
            raise ValidationError("You have not liked this post.")


def validate_date_format(value):
    """
    Validate the date format.
    """

    if value != datetime.strptime(value, "%d-%m-%Y").date():
            if settings.DEBUG:
                raise ValidationError("Invalid date format. Please use the format 'dd-mm-yyyy'.")
    return value


def validate_date(date_from, date_to):
    """
    Validate the date combination.
    """

    if date_from > date_to:
        if settings.DEBUG:
            raise ValidationError("Invalid date combination. Check again.")
        
