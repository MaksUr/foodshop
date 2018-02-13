import io

from PIL import Image
from django.contrib.auth.models import User
from django.core import urlresolvers
# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from meals.constants import MENU_POSITION_NAME, MENU_POSITION_NUTRITIONAL_VALUE, MENU_POSITION_PRICE, \
    MENU_POSITION_IMAGE
from meals.models import MenuPosition, CustomToken


class ApiTests(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('User', 'user@test.com', 'admin1234')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + CustomToken.KEY)

    def test_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + CustomToken.KEY)
        response = self.client.get(urlresolvers.reverse('api_menu_positions'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '1234asdvf')
        response = self.client.get(urlresolvers.reverse('api_menu_positions'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_menu_position(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))

        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        data = {
            MENU_POSITION_NAME: 'Пюрешечка',
            MENU_POSITION_NUTRITIONAL_VALUE: 200,
            MENU_POSITION_PRICE: 150.50,
            MENU_POSITION_IMAGE: file,
        }
        response = self.client.post(urlresolvers.reverse('api_menu_positions'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[MENU_POSITION_NAME], data[MENU_POSITION_NAME])
        self.assertEqual(response.data[MENU_POSITION_NUTRITIONAL_VALUE], data[MENU_POSITION_NUTRITIONAL_VALUE])
        self.assertEqual(response.data[MENU_POSITION_PRICE], '{:.2f}'.format(data[MENU_POSITION_PRICE]))
        self.assertEqual(MenuPosition.objects.count(), 1)





