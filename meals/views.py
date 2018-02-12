from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import FormView, ListView, DetailView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class MenuPositionList(APIView):
    def get(self, request, format=None):
        menu_positions = MenuPosition.objects.all()
        serializer = MenuPositionSerializer(menu_positions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MenuPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuPositionDetail(APIView):

    def get_object(self, pk):
        try:
            return MenuPosition.objects.get(pk=pk)
        except MenuPosition.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        menu_position = self.get_object(pk)
        serializer = MenuPositionSerializer(menu_position)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        menu_position = self.get_object(pk)
        serializer = MenuPositionSerializer(menu_position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        menu_position = self.get_object(pk)
        menu_position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)