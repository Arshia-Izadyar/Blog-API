from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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


class DetailPost(RetrieveUpdateDestroyAPIView):
    # model = PostModel
    permission_classes = []
    serializer_class = PostSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        print(pk)
        return PostModel.objects.filter(pk=pk)


class AddComment(CreateAPIView):
    model = CommentModel
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        pk = self.kwargs["pk"]
        post = PostModel.objects.get(pk=pk)
        if post.allow_comment(user):
            serializer.save(user=user, post=post)
        else:
            return Response({"Erorr": " can't add more that 3 comments"}, status=status.HTTP_406_NOT_ACCEPTABLE)
