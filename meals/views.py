from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView, ListView

from meals.forms import MenuPositionSelectForm
from meals.models import MenuPosition


class MenuPositionSelectFormView(FormView):
    success_url = 'order'
    form_class = MenuPositionSelectForm
    template_name = 'meals/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(MenuPositionSelectFormView, self).get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        r = form.add_order()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'query_set': r}))


class MenuPositionListView(ListView):
    model = MenuPosition

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        return res

