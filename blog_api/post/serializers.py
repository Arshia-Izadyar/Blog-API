from rest_framework import serializers
from django.contrib.auth import get_user_model


from .models import PostModel, CommentModel, LikeModel, DisLikeModel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = CommentModel
        fields = (
            "user",
            "comment",
        )


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = LikeModel
        fields = ("like", "user")


class DislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DisLikeModel
        fields = ("dislike", "user")


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        likes = obj.likes.filter(like=True).count()
        return likes

    def get_dislikes(self, obj):
        dislikes = obj.dislikes.filter(dislike=True).count()
        return dislikes

    class Meta:
        model = PostModel
        fields = ("id", "likes", "dislikes", "title", "body", "author", "comments")
