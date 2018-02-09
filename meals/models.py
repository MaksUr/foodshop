from django.db import models

# Create your models here.
from django.db.models import CharField, PositiveIntegerField, ImageField

from meals.constants import MENU_POSITION_NAME_KEY, MENU_POSITION_NUTRITIONAL_VALUE_KEY, MENU_POSITION_IMAGE_KEY, \
    MENU_POSITION_PRICE_KEY


class MenuPosition(models.Model):
    name = CharField(MENU_POSITION_NAME_KEY, max_length=45)
    nutritional_value = PositiveIntegerField(MENU_POSITION_NUTRITIONAL_VALUE_KEY)
    price = PositiveIntegerField(MENU_POSITION_PRICE_KEY)
    image = ImageField(MENU_POSITION_IMAGE_KEY, upload_to='meal_images/')

    def __str__(self):
        return self.name
