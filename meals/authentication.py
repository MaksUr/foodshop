from rest_framework.authentication import TokenAuthentication

from meals.models import CustomToken


class CustomAuthentication(TokenAuthentication):
    model = CustomToken
