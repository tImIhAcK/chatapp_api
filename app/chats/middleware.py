from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()


class TokenAuthentication:
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted'))

        return token.user


@database_sync_to_async
def get_user(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    # postpone model import to avoid ImproperlyConfigured error before Django
    # setup is complete.
    from django.contrib.auth.models import AnonymousUser

    if "token" not in scope:
        raise ValueError(
            "Cannot find token in scope. You should wrap your consumer in "
            "TokenAuthMiddleware."
        )
    token = scope["token"]
    user = None
    try:
        auth = TokenAuthentication()
        user = auth.authenticate(token)
    except AuthenticationFailed:
        pass
    return user or AnonymousUser()


@database_sync_to_async
def get_user2(user_id):
    from django.contrib.auth.models import AnonymousUser
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope["query_string"].decode())
        token = query_params.get('token', [''])[0]
        if not token:
            raise ValueError("Token is missing in the request URL")
        try:
            decoded_data = jwt_decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            untyped_token = UntypedToken(token)
            scope["user"] = await get_user2(decoded_data['user_id'])
            scope['token'] = untyped_token
        except (InvalidToken, TokenError) as e:
            print(f"Error decoding token: {e}")
            raise ValueError("Error decoding token")
        return await self.app(scope, receive, send)
