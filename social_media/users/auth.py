from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserRegistrationSerializer, UserProfileSerializer, CustomLoginSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

  #for sending mails and generate token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.db import IntegrityError





from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

@api_view(['POST'])
def registerUser(request):
    data = request.data
  
    User = get_user_model()

  
    if User.objects.filter(username=data['username']).exists():
        return Response({"details": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=data['email']).exists():
        return Response({"details": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)


    try:
     
        user = User.objects.create(
            username=data['username'], 
            email=data['email'], 
            password=make_password(data['password']),
            bio=data.get('bio', ''),
            is_active=False
        )

        
        email_subject = "Activate your account"
        message = render_to_string(
            "activate.html",
            {
                'user': user,
                'domain': '127.0.1.8000',  
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            }
        )
        
        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [data['email']]
        )
        email_message.send()

      
        serialize = UserRegistrationSerializer(user, many=False)
        return Response(serialize.data)

    except IntegrityError as e:
       
        return Response({"details": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
       
        return Response({"details": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])  
def forgot_password(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

        email_subject = "Reset your password"
        message = render_to_string("reset_password.html", {"link": link, "user": user})
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        return Response({"detail": "Password reset link sent to your email."})
    except User.DoesNotExist:
        return Response({"detail": "User not found with this email."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("password")
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been reset successfully."})

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not user.check_password(old_password):
        return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"detail": "Password changed successfully."})

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            return render(request,"activatesuccess.html")
        else:
            return render(request,"activatefail.html")
        
    
        

