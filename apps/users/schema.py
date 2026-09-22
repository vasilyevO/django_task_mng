from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme


class CookieJWTScheme(SimpleJWTScheme):
    target_class = 'apps.users.authentication.CookieJWTAuthentication'
    name = 'jwtAuth'
