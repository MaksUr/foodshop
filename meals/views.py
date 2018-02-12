from django.db.models import Sum
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import FormView, ListView, DetailView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from meals.authentication import CustomToken, CustomAuthentication
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


class MenuPositionList(ListCreateAPIView):
    queryset = MenuPosition.objects.all()
    serializer_class = MenuPositionSerializer


class MenuPositionDetail(RetrieveUpdateDestroyAPIView):
    queryset = MenuPosition.objects.all()
    serializer_class = MenuPositionSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (CustomAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = CustomToken.objects.get_or_create(user=user)
        return Response({'token': token.key})
