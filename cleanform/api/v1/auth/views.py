import jwt

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from cleanform.models.user import User
from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer
from .tasks import send_registration_email


@api_view(['GET'])
def user_status(request):
    if bool(request.user and request.user.is_authenticated):
        return Response(data={'detail': 'User is authenticated'}, status=status.HTTP_200_OK)
    else:
        return Response(data={'detail': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def registration_email(request):
    email = request.GET.get('email', None)
    resend = request.GET.get('resend', False)

    if not email:
        return Response(data={'detail': 'Please provide email address'}, status=status.HTTP_400_BAD_REQUEST)

    # Task - Email Registration
    send_registration_email.delay(email)

    return Response(data={'detail': 'Registration email send!'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def get(self, request):
        registration_token = request.query_params.get('token', None)
        if not registration_token:
            return Response(data={'detail': 'Registration token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Verifying and decoding token
        try:
            verified_email = jwt.decode(registration_token, settings.SECRET_KEY, algorithms="HS256").get('email')

            return Response(data={'detail': 'Registration token is valid', 'email': verified_email}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'Registration token has been expired!'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        register_serializer = RegisterSerializer(data=request.data)
        registration_token = request.query_params.get('token', None)

        # Checking for registration token
        if not registration_token:
            return Response(data={'detail': 'Registration token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Checking for valid request body
        if not register_serializer.is_valid():
            return Response(data={'detail': 'Invalid data submission'}, status=status.HTTP_400_BAD_REQUEST)

        new_user_credentials = register_serializer.data
        email = register_serializer.data.get('email')

        # Verifying and decoding token
        try:
            verified_email = jwt.decode(registration_token, settings.SECRET_KEY, algorithms="HS256").get('email')
            if email != verified_email:
                return Response(data={'detail': 'Registration token and email mismatch'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'Registration token has been expired!'}, status=status.HTTP_401_UNAUTHORIZED)

        # Checking for existing account
        try:
            User.objects.get(email=email)
            return Response(data={'detail': 'Account exists with current email address'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            password = new_user_credentials.pop('password')
            confirm_password = new_user_credentials.pop('confirm_password')

            # Checking for password and confirm password
            if password != confirm_password:
                return Response(data={'detail': 'Password and confirm password are not equal'}, status=status.HTTP_400_BAD_REQUEST)

            # Creating a new user
            user = User(**new_user_credentials)
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


@api_view(['POST'])
def register_view(request):
    register_serializer = RegisterSerializer(data=request.data)
    registration_token = request.query_params.get('token', None)

    # Checking for registration token
    if not registration_token:
        return Response(data={'detail': 'Registration token is missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Checking for valid request body
    if not register_serializer.is_valid():
        return Response(data={'detail': 'Invalid data submission'}, status=status.HTTP_400_BAD_REQUEST)

    new_user_credentials = register_serializer.data
    email = register_serializer.data.get('email')

    # Verifying and decoding token
    try:
        verified_email = jwt.decode(registration_token, settings.SECRET_KEY, algorithms="HS256").get('email')
        if email != verified_email:
            return Response(data={'detail': 'Registration token and email mismatch'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError:
        return Response(data={'detail': 'Registration token has been expired!'}, status=status.HTTP_401_UNAUTHORIZED)

    # Checking for existing account
    try:
        User.objects.get(email=email)
        return Response(data={'detail': 'Account exists with current email address'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        password = new_user_credentials.pop('password')
        confirm_password = new_user_credentials.pop('confirm_password')

        # Checking for password and confirm password
        if password != confirm_password:
            return Response(data={'detail': 'Password and confirm password are not equal'}, status=status.HTTP_400_BAD_REQUEST)

        # Creating a new user
        user = User(**new_user_credentials)
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
