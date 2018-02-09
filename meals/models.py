from django.db import models

# Create your models here.
from django.db.models import CharField, PositiveIntegerField, ImageField

from meals.constants import MEAL_NAME_KEY, MEAL_NUTRITIONAL_KEY, MEAL_IMAGE_KEY


class Meal(models.Model):
    name = CharField(MEAL_NAME_KEY, max_length=45)
    nutritional_value = PositiveIntegerField(MEAL_NUTRITIONAL_KEY)
    price = PositiveIntegerField(MEAL_NUTRITIONAL_KEY)
    image = ImageField(MEAL_IMAGE_KEY, upload_to='meal_images/')
