from django.urls import path
from .auth import CustomTokenObtainPairView, CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    FollowUserView,
    UnfollowUserView,
    UserListView,
)
from .auth import(
    registerUser,
    ActivateAccountView,
    forgot_password,
    reset_password_confirm,
    change_password,
    CustomLoginView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),

    #auth paths
    path('users/register/',registerUser,name='register'),
    path('acitvate/<uidb64>/<token>', ActivateAccountView.as_view(),name='activate'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", reset_password_confirm, name="reset_password_confirm"),
    path("change-password/", change_password, name="change_password"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]