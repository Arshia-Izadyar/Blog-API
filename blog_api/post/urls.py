from rest_framework.urls import path

from .views import PostListCreateView, AddComment, DetailPost, AddLike, AddDisLike

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="post-list"),
    path("post/<int:pk>/", DetailPost.as_view(), name="post-detail"),
    path("post/<int:pk>/comment/", AddComment.as_view(), name="add-comment"),
    path("post/<int:pk>/like/", AddLike.as_view(), name="add-like"),
    path("post/<int:pk>/dislike/", AddDisLike.as_view(), name="disadd-like"),
]
