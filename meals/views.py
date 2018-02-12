from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, DetailView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from meals.constants import MENU_POSITION_PAGINATE_BY
from meals.forms import MenuPositionSelectForm, MenuPositionForm
from meals.models import MenuPosition, Order
from meals.serializers import MenuPositionSerializer


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


class NewMenuPositionView(FormView):
    form_class = MenuPositionForm
    template_name = "meals/new_menu_position.html"

    def form_valid(self, form):
        obj = form.save()
        self.success_url = obj.get_absolute_url()
        return super().form_valid(form)


class MenuPositionDetailView(DetailView):
    model = MenuPosition
    pass


@api_view(['GET', 'POST'])
def menu_position_list(request, format=None):
    if request.method == 'GET':
        menu_positions = MenuPosition.objects.all()
        serializer = MenuPositionSerializer(menu_positions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def menu_position_detail(request, pk, format=None):
    try:
        menu_positions = MenuPosition.objects.get(pk=pk)
    except MenuPosition.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MenuPositionSerializer(menu_positions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MenuPositionSerializer(menu_positions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        menu_positions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)