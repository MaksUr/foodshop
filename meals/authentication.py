from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


class CustomToken(Token):
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = 'my_token'
        return super(Token, self).save(*args, **kwargs)


class CustomAuthentication(TokenAuthentication):
    model = CustomToken
