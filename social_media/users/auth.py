from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect
from .serializers import UserSerializer,UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
# for sending mails and generate token
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import TemplateView
import string
import random
import secrets



User = get_user_model()

@csrf_exempt
@api_view(['GET'])
def getRoutes(request):
    return Response('Hello GDG')




@csrf_exempt
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v       
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

User = get_user_model()
@api_view(['POST'])
def loginUser(request):

    email = request.data.get('email')
    password = request.data.get('password')

   
    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    user = authenticate(request, username=email, password=password)

    
    if user is None or not user.is_active:
        raise AuthenticationFailed("Invalid credentials or account is inactive")

    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    
    return Response({
        'refresh': str(refresh),
        'access': access_token
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  getUserProfiles(request):
    user=request.user
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)
@csrf_exempt
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'Email address already registered.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=data['username'],
            bio=data['bio'],
            email=data['email'],
            password=make_password(data['password']),
            is_active=False
        )

        email_subject = "Activate Your Account"
        message = render_to_string(
            "activate.html",
            {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            }
        )

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [data['email']])
        email_message.send()

        return Response({'message': 'User registered successfully.Please Verify your Email, Email Verification is sent.'}, status=status.HTTP_201_CREATED)

    except KeyError as e:
        return Response(
            {'error': f'Missing field: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
def activate_account_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "activatesuccess.html")
    else:
        return render(request, "activatefail.html")
    


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')

        if not email:
            return Response(
                {'error': 'Email field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            
            User = get_user_model()
            user = User.objects.filter(email=email).first()

            if user:
                
                new_password = generate_random_password()

                
                user.set_password(new_password)
                user.save()

                
                email_subject = "Your New Password"
                message = f"Hello {user.username},\n\nYour new password is: {new_password}\n\nPlease use this password to log in and change it after you log in."

                
                send_mail(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                return Response(
                    {'message': 'New password has been sent to your email.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'No user found with that email address in the Users table.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

