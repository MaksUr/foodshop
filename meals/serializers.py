from rest_framework import serializers

from meals.constants import MENU_POSITION_NAME, MENU_POSITION_NUTRITIONAL_VALUE, MENU_POSITION_PRICE, \
    MENU_POSITION_IMAGE
from meals.models import MenuPosition


class MenuPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuPosition
        fields = (MENU_POSITION_NAME, MENU_POSITION_NUTRITIONAL_VALUE, MENU_POSITION_PRICE)


