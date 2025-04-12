from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model() 
        try:
            # Try to get the user by email
            user = User.objects.get(email=username)
        except ObjectDoesNotExist:
            return None

        # Check if the password matches
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
