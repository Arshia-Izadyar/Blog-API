from rest_framework import serializers
from django.contrib.auth import get_user_model


from .models import PostModel, CommentModel

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('comment',)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = PostModel
        fields = ('id', 'title', 'body','author', 'comments')
        
        
