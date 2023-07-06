from rest_framework.urls import path

from .views import PostListCreateView, AddComment

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/comment/', AddComment.as_view(), name='add-comment'),
    
]
