from django import forms
from django.forms import ChoiceField, ModelMultipleChoiceField
from django.forms.models import ModelChoiceIterator

from meals.constants import MENU_POSITION_NAME, MENU_POSITION_NUTRITIONAL_VALUE, MENU_POSITION_PRICE, \
    MENU_POSITION_IMAGE, MENU_POSITION_NAME_HELP, MENU_POSITION_NUTRITIONAL_VALUE_HELP, MENU_POSITION_PRICE_HELP, \
    MENU_POSITION_IMAGE_HELP
from meals.models import MenuPosition, Order, MenuPositionInOrder


class AdvancedModelChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return self.field.prepare_value(obj), self.field.label_from_instance(obj), obj,


class AdvancedModelMultipleChoiceField(ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices

        return AdvancedModelChoiceIterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)


class MenuPositionSelectForm(forms.Form):
    menu_positions = AdvancedModelMultipleChoiceField(queryset=MenuPosition.objects.all(), required=True)

    def add_order(self):
        menu_positions = self.cleaned_data.get('menu_positions')
        order = Order.objects.create()
        for menu_position in menu_positions:
            MenuPositionInOrder.objects.create(menu_position=menu_position, order=order)
        return order


class MenuPositionForm(forms.ModelForm):
    class Meta:
        model = MenuPosition
        fields = (
            MENU_POSITION_NAME,
            MENU_POSITION_NUTRITIONAL_VALUE,
            MENU_POSITION_PRICE,
            MENU_POSITION_IMAGE,
        )

        help_texts = {
            MENU_POSITION_NAME: MENU_POSITION_NAME_HELP,
            MENU_POSITION_NUTRITIONAL_VALUE: MENU_POSITION_NUTRITIONAL_VALUE_HELP,
            MENU_POSITION_PRICE: MENU_POSITION_PRICE_HELP,
            MENU_POSITION_IMAGE: MENU_POSITION_IMAGE_HELP,
        }


