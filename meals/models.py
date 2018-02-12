from django.db import models

# Create your models here.
from django.db.models import CharField, PositiveIntegerField, ImageField, DecimalField, ForeignKey
from django.urls import reverse

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


