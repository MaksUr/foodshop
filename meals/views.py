from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView, ListView

from meals.forms import MenuPositionSelectForm
from meals.models import MenuPosition


class MenuPositionSelectFormView(FormView):
    success_url = '/order/'
    form_class = MenuPositionSelectForm
    template_name = 'meals/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(MenuPositionSelectFormView, self).get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        form.calculate_order()
        return super(MenuPositionSelectFormView, self).form_valid(form)


class MenuPositionListView(ListView):
    model = MenuPosition

