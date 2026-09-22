from django.conf import settings
from rest_framework.response import Response


def set_auth_cookies(
    response: Response, access: str, refresh: str | None = None,
) -> None:
    """Кладёт access/refresh в httpOnly cookies."""
    lifetimes = settings.SIMPLE_JWT
    params = {
        'httponly': True,
        'secure': settings.AUTH_COOKIE_SECURE,
        'samesite': settings.AUTH_COOKIE_SAMESITE,
    }
    response.set_cookie(
        settings.AUTH_COOKIE_ACCESS,
        access,
        max_age=int(lifetimes['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        path='/',
        **params,
    )
    if refresh is not None:
        response.set_cookie(
            settings.AUTH_COOKIE_REFRESH,
            refresh,
            max_age=int(lifetimes['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            path=settings.AUTH_COOKIE_REFRESH_PATH,
            **params,
        )


def delete_auth_cookies(response: Response) -> None:
    """Удаляет cookies с токенами."""
    response.delete_cookie(settings.AUTH_COOKIE_ACCESS, path='/')
    response.delete_cookie(
        settings.AUTH_COOKIE_REFRESH, path=settings.AUTH_COOKIE_REFRESH_PATH,
    )
