from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.cookies import delete_auth_cookies, set_auth_cookies
from apps.users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


def _refresh_from_request(request: Request) -> str | None:
    return (
        request.data.get('refresh')
        or request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)
    )


class RegisterView(generics.CreateAPIView):
    """POST — регистрация нового пользователя"""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class LoginView(generics.GenericAPIView):
    """POST — вход: выдаёт access/refresh и кладёт их в httpOnly cookies"""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        response = Response({
            'user': UserSerializer(user).data,
            'access': access,
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
        set_auth_cookies(response, access, str(refresh))
        return response


class CookieTokenRefreshView(generics.GenericAPIView):
    """POST — новый access по refresh из cookie (или из тела запроса)"""

    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(
            data={'refresh': _refresh_from_request(request)},
        )
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = serializer.validated_data
        response = Response(data, status=status.HTTP_200_OK)
        set_auth_cookies(response, data['access'], data.get('refresh'))
        return response


class LogoutView(generics.GenericAPIView):
    """POST — выход: refresh в blacklist, cookies удаляются"""

    serializer_class = TokenBlacklistSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(
            data={'refresh': _refresh_from_request(request)},
        )
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(
            {'detail': 'Successfully logged out.'},
            status=status.HTTP_200_OK,
        )
        delete_auth_cookies(response)
        return response


class MeView(generics.RetrieveAPIView):
    """GET — текущий пользователь"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
