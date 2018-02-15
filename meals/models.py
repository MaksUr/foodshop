from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import CharField, PositiveIntegerField, ImageField, DecimalField, ForeignKey
from django.urls import reverse
from rest_framework.authtoken.models import Token

from foodShop.settings import SECRET_KEY
from meals.constants import MENU_POSITION_NAME_KEY, MENU_POSITION_NUTRITIONAL_VALUE_KEY, MENU_POSITION_IMAGE_KEY, \
    MENU_POSITION_PRICE_KEY, MENU_POSITION_MAX_LENGTH


class CustomToken(models.Model):
    KEY = SECRET_KEY
    key = models.CharField(_("Key"), max_length=40)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return self.KEY

    def __str__(self):
        return self.key


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


