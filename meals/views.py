from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from meals.constants import MENU_POSITION_PAGINATE_BY
from meals.models import MenuPosition


class MenuPositionListView(ListView):
    model = MenuPosition
    paginate_by = MENU_POSITION_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context_data = super(MenuPositionListView, self).get_context_data(**kwargs)
        return context_data
