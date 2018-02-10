from django.test import TestCase

# Create your tests here.
from meals.models import MenuPosition


class MealMethodTests(TestCase):

    def setUp(self):
        MenuPosition.objects.create(name="Фуагра", nutritional_value=100, price=240, image='meal_images/1.jpg')
        MenuPosition.objects.create(name="Котлетка", nutritional_value=200, price=210, image='meal_images/2.jpg')
        MenuPosition.objects.create(name="Пюрешка", nutritional_value=200, price=210, image='meal_images/3.jpg')

    def test_check_crate(self):

        MenuPosition.objects.get(name="Фуагра")
        MenuPosition.objects.get(name="Котлетка")
        MenuPosition.objects.get(name="Пюрешка")

