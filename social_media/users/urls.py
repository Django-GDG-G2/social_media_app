from django.urls import path
from .auth import ForgotPasswordAPIView

from users.auth import loginUser
from rest_framework_simplejwt.views import TokenRefreshView
from .auth import(
    getUserProfiles,
    getUsers,
    registerUser,
    activate_account_view,
    loginUser,

 

)
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    FollowUserView,
    UnfollowUserView,
    UserListView,

    UserRegistrationTemplateView,
    UserLoginTemplateView,
    UserLogoutTemplateView,
    UserProfileTemplateView,
    UserListTemplateView,

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


urlpatterns = [

    
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('api/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('api/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    # Template rendering URLs
    path('register/', UserRegistrationTemplateView.as_view(), name='register'),
    path('login/', UserLoginTemplateView.as_view(), name='login'),
    path('logout/', UserLogoutTemplateView.as_view(), name='logout'),
    path('users/', UserListTemplateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserProfileTemplateView.as_view(), name='user-profile'),

    

    #auth paths
    path('users/profile/',getUserProfiles,name="getUserProfiles"),
    path('users/',getUsers,name="getUsers"),
    path('users/login/', loginUser, name='login'),
    path('users/register/',registerUser,name="register"),
    path('activate/<uidb64>/<token>', activate_account_view, name='activate'),
   
    path('password-reset/', ForgotPasswordAPIView.as_view(), name='password_reset'),




   

]

