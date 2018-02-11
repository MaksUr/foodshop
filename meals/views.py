from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView, ListView

from meals.constants import MENU_POSITION_PAGINATE_BY
from meals.forms import MenuPositionSelectForm
from meals.models import MenuPosition, Order


class MenuPositionSelectFormView(FormView):
    form_class = MenuPositionSelectForm
    template_name = 'meals/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(MenuPositionSelectFormView, self).get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        order = form.add_order()
        self.success_url = order.get_absolute_url()
        return super().form_valid(form)


class MenuPositionInOrderListView(ListView):
    model = MenuPosition
    paginate_by = MENU_POSITION_PAGINATE_BY

    def get_queryset(self):
        order = get_object_or_404(Order, id=self.kwargs.get('pk'))
        queryset = MenuPosition.objects.filter(menupositioninorder__order=order)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: count total price
        context['total_price'] = self.object_list.aggregate(Sum('price')).get('price__sum')
        return context

