# RestFramework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# SimpleJWT
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Local
from .models import Client
from .serializers import (
    RegistrationSerializer, 
    AuthSerializer,
)
from abstract.mixins import ResponseMixin


@permission_classes([AllowAny])
class AuthorizationView(TokenObtainPairView, ResponseMixin):
    """Custom view for authorization."""

    def post(self, request: Request) -> Response:
        """POST method for authorization."""

        serializer: AuthSerializer =\
            AuthSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        username: str = serializer.validated_data.get('username')
        password: str = serializer.validated_data.get('password')

        try:
            user = Client.objects.get(username=username)
            if user.is_active:
                if not user.check_password(password):
                    return self.get_response(
                        key='error',
                        data='Invalid Password',
                        status='400'
                    )
                try:
                    access_token = AccessToken.for_user(user)
                    refresh_token = RefreshToken.for_user(user)
                except TokenError as e:
                    return self.get_response(
                        key='error',
                        data=str(e),
                        status='400'
                    )
                return self.get_response(
                    key='Success',
                    data={
                        'access' : str(access_token),
                        'refresh' : str(refresh_token),
                        'username' : str(user.username)
                    },
                    status='200'
                )
            return self.get_response(
                key='error',
                data='Аккаунт не активирован',
                status='400'
            )
        except Client.DoesNotExist:
            return self.get_response(
                key='error',
                data='Пользователь с таким username не существует',
                status='400'
            )


@permission_classes([AllowAny])
class RegistrationView(APIView, ResponseMixin):
    """View For Registration."""

    def post(self, request: Request) -> Response:
        """POST method for registration."""

        serializer: RegistrationSerializer =\
            RegistrationSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.get_response(
            key='Registration',
            data='Success',
            status='200'
        )
        
