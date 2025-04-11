from django.urls import path
from .views import (PostCreateView, PostDetailView, CommentListCreateApiView
                    , CommentDetail, LikeCreateApiView, unlike)

urlpatterns = [
            # create/update/delete/retrive a post
    path('post/create/', PostCreateView.as_view(), name='post-detail'),  # TO CREATE POST USING (POST), AND LIST OF ALL POSTS USING [GET] METHOD
    path('post/detail/<int:post_id>/', PostDetailView.as_view(), name='post-detail'), # TO UPDATE, DELETE, AND DETAIL VIEW POST RESPECTIVELY[PUT, DELETE, GET]

         # for comments
    path('comments/', CommentListCreateApiView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
        # for likes
    path('like/post/<int:pk>/', LikeCreateApiView.as_view(), name='user-like' ),
    path('unlike/post/<int:pk>/', unlike.as_view(), name='user-unlike' ),
]