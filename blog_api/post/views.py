from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.core.exceptions import ValidationError

from .models import PostModel, CommentModel
from .serializers import PostSerializer, CommentSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = PostModel.objects
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class AddComment(CreateAPIView):
    model = CommentModel
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    
    def perform_create(self, serializer):
        user = self.request.user
        pk = self.kwargs['pk']
        post = PostModel.objects.get(pk=pk)
        if post.allow_comment(user):
            serializer.save(user=user, post=post)
        else:
            raise ValidationError('can\'t add more than 3 comments')
    