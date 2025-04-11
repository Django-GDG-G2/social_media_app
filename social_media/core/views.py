from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions
from .models import Post, Like, Comment
from users.views import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.exceptions import ValidationError
from .serializers import (PostDetailSerializer, PostSerailzer, 
                          CommentSerializer, LikeSerializer)






User = get_user_model()



            # Post (CRUD)



class PostCreateView(generics.GenericAPIView):


    queryset = Post.objects.all()
    serializer_class = PostSerailzer
    permission_classes = [permissions.IsAuthenticated]  

   # GETS ALL POSTS AVAILABLE ...

    @swagger_auto_schema(operation_summary="List all Posts made ")

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)  # Fixed instance passing

        return Response(serializer.data, status=status.HTTP_200_OK)
    

   # CREATAE A POST...

    @swagger_auto_schema(operation_summary="Create a new post ")

    def post(self, request):
        serializer = self.serializer_class(

            data=request.data,  
            context={'author': request.user} 
        )
        
        user = request.user

        if serializer.is_valid():
            serializer.save(author=user) 

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


                # Post detail, update, and delete view
                        # CRUD OPERATIONS  👇


class PostDetailView(generics.GenericAPIView):

    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]

   # GETS DETAIL VIEW WITH AN ID

    @swagger_auto_schema(operation_summary="Retrive a post by it's id")

    def get(self, request, post_id):


        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # UPDATES A POST WITH A SPECIFIC ID

    @swagger_auto_schema(operation_summary="update a post by it's id")


    def put(self, request, post_id):

        queryset = Post.objects.all()
        serializer_class = PostDetailSerializer


        try:
            instance = Post.objects.get(pk=post_id)  # Direct query instead of get_queryset()
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   # DELETE A POST WITH AN ID

    @swagger_auto_schema(operation_summary="Delete a post by it's id")

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        
        post.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)
    


        # comments section

class CommentListCreateApiView(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):

        if self.request.user != self.get_object().user:
            raise PermissionError("You can't edit someone else's comment.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user != self.get_object().user:
            raise PermissionError("you can't delete someone else's comment.")
        instance.delete()


             #like a post

class LikeCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user

                    # Check if the user has already liked the post
            if Like.objects.filter(post=post, user=user).exists():
                return Response({'error': "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
            
             # Create a like
            new_like, created = Like.objects.get_or_create(user=user, post=post)

            # Serialize the newly created like
            serializer = LikeSerializer(new_like)

            # Extract data to show nice message
            data = serializer.data
            msg = f"{data['author_username']} liked post 🤙 '{data['post_id']}' created by {data['post_author']}"
            return Response({"message": msg}, status=status.HTTP_201_CREATED)
        
        except Post.DoesNotExist:
            return Response({'error post not found'}, status=status.HTTP_404_NOT_FOUND)


   
class unlike(generics.GenericAPIView):
    queryset = Post.objects.all()  # Query for the Post model
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            # post = self.get_object()  # Get the Post object using `pk`
            post = generics.get_object_or_404(Post, pk=pk)
            user = request.user

            # Check if the user has liked the post
            likes = Like.objects.filter(post=post, user=user).first()
            if not likes:
                return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

            # Remove the like
            Like.delete()

            return Response({"success": "Post unliked successfully"}, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({'error': "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)