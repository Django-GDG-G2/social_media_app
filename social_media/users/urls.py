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
   
    UserLogoutView,
    UserProfileView,
    FollowUserView,
    UnfollowUserView,
    UserListView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


urlpatterns = [
    
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    

    #auth paths
    path('users/profile/',getUserProfiles,name="getUserProfiles"),
    path('users/',getUsers,name="getUsers"),
    path('users/login/', loginUser, name='login'),
    path('users/register/',registerUser,name="register"),
    path('activate/<uidb64>/<token>', activate_account_view, name='activate'),
   
    path('password-reset/', ForgotPasswordAPIView.as_view(), name='password_reset'),




   

]