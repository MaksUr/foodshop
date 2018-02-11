from os.path import join, isdir

from os import listdir

import re

from foodShop.settings import BASE_DIR
from meals.models import MenuPosition

PATTERN_MENU_POSITION_NAME = re.compile(r'(\w+)_nv(\d+)_p(\d+)')


def parse_menu_position_name(name):
    m = re.match(PATTERN_MENU_POSITION_NAME, name)
    if m:
        return m.group(1), m.group(2), m.group(3)


def create_test_positions():
    images_pth = join(BASE_DIR, 'media', 'meal_images')
    if not isdir(images_pth):
        return
    images = listdir(images_pth)
    for name_image in images:
        r = parse_menu_position_name(name_image)
        if not r:
            continue
        name, nutr_val, price = r
        MenuPosition.objects.create(
            name=name, nutritional_value=nutr_val,
            price=price, image='/media/meal_images/' + name_image
        )
