from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PostModel(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def allow_comment(self, user):
        user_comments = self.comments.filter(
            user=user,
        )
        current_count = user_comments.count()
        if current_count < 3:
            return True
        else:
            return False


class CommentModel(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(PostModel, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)


class LikeModel(models.Model):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, related_name="likes", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post)


class DisLikeModel(models.Model):
    user = models.ForeignKey(User, related_name="dislikes", on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, related_name="dislikes", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post)
