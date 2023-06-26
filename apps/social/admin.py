from django.contrib import admin

from apps.social.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "created", "updated", "total_likes")
    filter_horizontal = ("user_likes",)
