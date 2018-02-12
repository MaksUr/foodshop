from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

# Create your models here.
from django.db.models import CharField, PositiveIntegerField, ImageField, DecimalField, ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token

from meals.authentication import CustomToken
from meals.constants import MENU_POSITION_NAME_KEY, MENU_POSITION_NUTRITIONAL_VALUE_KEY, MENU_POSITION_IMAGE_KEY, \
    MENU_POSITION_PRICE_KEY, MENU_POSITION_MAX_LENGTH


class MenuPosition(models.Model):
    name = CharField(MENU_POSITION_NAME_KEY, max_length=MENU_POSITION_MAX_LENGTH)
    nutritional_value = PositiveIntegerField(MENU_POSITION_NUTRITIONAL_VALUE_KEY)
    price = DecimalField(MENU_POSITION_PRICE_KEY, max_digits=10, decimal_places=2)
    image = ImageField(MENU_POSITION_IMAGE_KEY, upload_to='meal_images')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu_position', kwargs={'pk': self.id})


class Order(models.Model):
    def get_absolute_url(self):
        return reverse('order', kwargs={'pk': self.id})


class MenuPositionInOrder(models.Model):
    menu_position = ForeignKey(MenuPosition)
    order = ForeignKey(Order)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    print('tooooken')
    if created:
        CustomToken.objects.create(user=instance)

