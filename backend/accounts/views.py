from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


def first_error(errors):
    """Flatten DRF's error dict into a single readable message."""
    for value in errors.values():
        if isinstance(value, list) and value:
            return str(value[0])
    return 'Invalid input.'


def token_for(user):
    return str(RefreshToken.for_user(user).access_token)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': first_error(serializer.errors)}, status=400)
        user = serializer.save()
        return Response(
            {'token': token_for(user), 'user': UserSerializer(user).data},
            status=201
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        password = request.data.get('password') or ''

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=400)

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': "That email and password don't match any account."}, status=401)

        return Response({'token': token_for(user), 'user': UserSerializer(user).data})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
