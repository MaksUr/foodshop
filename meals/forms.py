from django import forms
from django.forms import ChoiceField, ModelMultipleChoiceField
from django.forms.models import ModelChoiceIterator

from meals.models import MenuPosition


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
        # TODO: create order
        # TODO: add positions to order
        return order_id



