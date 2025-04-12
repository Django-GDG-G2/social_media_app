from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Follow, User
from rest_framework_simplejwt.views import TokenObtainPairView



# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
   
    class Meta:
        model=User
        
        fields = ['id','email', 'username', 'password', 'bio','isAdmin']
    
    def get_name(self,obj):
        firstname=obj.first_name
        lastname=obj.last_name
        name=firstname+' '+lastname
        if name=='':
            name=obj.email[:5]
            return name
        return name
    
    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

    
class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields = ['id','_id','email', 'username', 'password', 'bio','isAdmin','token']
    
    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)   


    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.BooleanField(read_only=True) 
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'bio','isAdmin')

    def create(self, validated_data):

        user = User.objects.create_user(
        email=validated_data['email'],
        username=validated_data['username'],
        password=validated_data['password'],
        bio=validated_data.get('bio', '')
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise serializers.ValidationError("Account is not activated. Please verify your email.")
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise serializers.ValidationError("Account inactive. Please check your email to activate your account.")

        data['username'] = self.user.username
        data['isAdmin'] = self.user.isAdmin
        return data
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(max_length=None, use_url=True)
    isAdmin = serializers.BooleanField(source='isAdmin')
    class Meta:
        model = User
        fields = (
            'id', 'bio', 'profile_picture',
            'followers_count', 'following_count',
            'date_joined'
        )

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()



class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
        read_only_fields = ('follower', 'created_at')
