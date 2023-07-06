from django.contrib import admin

from .models import PostModel, CommentModel, LikeModel, DisLikeModel


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    search_fields = (
        "author",
        "title",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
