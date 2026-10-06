from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import SessionToken
from django.utils import timezone


class SessionTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = SessionToken

    def get_model(self):
        return self.model

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(token=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.is_valid():
            raise AuthenticationFailed('Token expired.')

        if not token.user.is_active:
            raise AuthenticationFailed('User account is inactive.')

        return (token.user, token)
