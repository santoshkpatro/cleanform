import jwt
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from rest_framework import generics, status, serializers, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from tzapp.models.user import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    full_name = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'phone',
            'avatar',
            'avatar_url'
        ]


@api_view(['GET'])
def registration_email(request):
    email = request.GET.get('email', None)
    resend = request.GET.get('resend', False)

    if not email:
        return Response(data={'detail': 'Please provide email address'}, status=status.HTTP_400_BAD_REQUEST)

    payload = {
        'email': email,
        'exp': timezone.now() + timezone.timedelta(minutes=10)
    }
    encoded = jwt.encode(payload=payload, key=settings.SECRET_KEY)

    # Send an email
    print(encoded)
    
    return Response(data={'detail': 'Registration email send!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_view(request):
    register_serializer = RegisterSerializer(data=request.data)

    # Checking for valid request body
    if not register_serializer.is_valid():
        return Response(data={'detail': 'Invalid data submission'}, status=status.HTTP_400_BAD_REQUEST)

    new_user_credentials = register_serializer.data
    email = register_serializer.data.get('email')

    try:
        # Checking for existing account
        User.objects.get(email=email)

        return Response(data={'detail': 'Account exists with current email address'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        password = new_user_credentials.pop('password')
        confirm_password = new_user_credentials.pop('confirm_password')
        
        # Checking for password and confirm password
        if password != confirm_password:
            return Response(data={'detail': 'Password and confirm password are not equal'}, status=status.HTTP_400_BAD_REQUEST)

        # Creating a new user
        user = User.objects.create(**new_user_credentials)
        user.set_password(password)
        user.save()

        return Response(data={'detail': 'Account creation success'}, status=status.HTTP_201_CREATED)

        
@api_view(['POST'])
def login_view(request):
    login_serializer = LoginSerializer(data=request.data)
    
    # Checking for valid request body
    if not login_serializer.is_valid():
        return Response(data={'detail': 'Invalid data submission'}, status=status.HTTP_400_BAD_REQUEST)

    credentials = login_serializer.data

    # Checking for correct email and password
    user = authenticate(**credentials)

    # If not user found
    if not user:
        return Response(data={'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    # If password reset is required
    if user.password_reset_required:
        return Response(data={'detail': 'Password reset required', 'password_reset_required': True}, status=status.HTTP_200_OK)

    # JWT access and refresh token
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    
    return Response(data={
        'detail': 'Login success', 
        'access_token': str(access_token), 
        'refresh_token': str(refresh_token), 
        'password_reset_required': False}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        authenticated_user = self.request.user
        return authenticated_user