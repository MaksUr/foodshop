from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver

from meals.authentication import CustomToken


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    print('tooooken')
    if created:
        CustomToken.objects.create(user=instance)