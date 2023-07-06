from rest_framework.urls import path

from .views import PostListCreateView, AddComment, DetailPost

urlpatterns = [
    path("post/", PostListCreateView.as_view(), name="post-list"),
    path("post/<int:pk>/", DetailPost.as_view(), name="post-detail"),
    path("posts/<int:pk>/comment/", AddComment.as_view(), name="add-comment"),
]
