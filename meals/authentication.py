from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token

from foodShop.settings import SECRET_KEY


class CustomToken(Token):
    def generate_key(self):
        print('generate_token')
        return SECRET_KEY


class CustomAuthentication(TokenAuthentication):
    model = CustomToken
