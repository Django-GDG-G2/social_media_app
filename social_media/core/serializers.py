from .models import Post, Comment, Like
from rest_framework import serializers



class PostSerailzer(serializers.ModelSerializer):

    post_id = serializers.ReadOnlyField(source='id')  # renaming id of the post to post_id for clarity

    class Meta:
        model = Post
        fields = ['post_id', 'author', 'title', 'content', 'media', 'created_at']
        read_only_fields = ['post_id', 'author', 'created_at']  #this fields can't be set by the api user
        depth = 1   #shows authors username...


class PostDetailSerializer(serializers.ModelSerializer):

    post_id = serializers.ReadOnlyField(source='id')  # renaming id of the post to post_id for clarity

    class Meta:
        model = Post
        fields = ['post_id', 'author', 'title', 'content', 'media']
        depth = 1   #shows authors username...

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='user.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'post_title', 'post_id', 'comment', 'created_at']
    
class LikeSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='user.username', read_only=True)
    post_author = serializers.CharField(source='post.author.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'author_username', 'post_author', ]
        read_only_fields = ['id', 'author_username', 'created_at']