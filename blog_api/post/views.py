from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsAuthorOrReadOnly
from .models import PostModel, CommentModel, LikeModel, DisLikeModel
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, DislikeSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = PostModel.objects
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class DetailPost(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return PostModel.objects.filter(pk=pk)


class AddComment(CreateAPIView):
    model = CommentModel
    queryset = (
        CommentModel.objects
    )  # added query set to prevent swagger error: (view's AddComment raised exception during schema generation)

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        pk = self.kwargs["pk"]
        post = PostModel.objects.get(pk=pk)
        # post = get_object_or_404(PostModel, pk)
        if post.allow_comment(user):
            serializer.save(user=user, post=post)
        else:
            return Response({"Erorr": " can't add more that 3 comments"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class AddLike(CreateAPIView):
    model = LikeModel
    queryset = LikeModel.objects
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        post = PostModel.objects.get(pk=pk)
        serializer.save(user=self.request.user, post=post)


class AddDisLike(CreateAPIView):
    model = DisLikeModel
    queryset = DisLikeModel.objects

    permission_classes = [IsAuthenticated]
    serializer_class = DislikeSerializer

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        post = PostModel.objects.get(pk=pk)
        serializer.save(user=self.request.user, post=post)
