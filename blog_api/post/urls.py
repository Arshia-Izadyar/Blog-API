from rest_framework.urls import path


from .views import PostListCreateView, AddComment, DetailPost, AddLike, AddDisLike

urlpatterns = [
    path("list/", PostListCreateView.as_view(), name="post-list"),
    path("<int:pk>/detail/", DetailPost.as_view(), name="post-detail"),
    path("<int:pk>/comment/", AddComment.as_view(), name="add-comment"),
    path("<int:pk>/like/", AddLike.as_view(), name="add-like"),
    path("<int:pk>/dislike/", AddDisLike.as_view(), name="disadd-like"),
    
]


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

