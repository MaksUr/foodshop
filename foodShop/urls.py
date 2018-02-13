"""foodShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from foodShop import settings
from meals.views import MenuPositionSelectFormView, MenuPositionInOrderListView, NewMenuPositionView, \
    MenuPositionDetailView, MenuPositionList, MenuPositionDetail, CustomObtainAuthToken

urlpatterns = [
    url(r'^$', MenuPositionSelectFormView.as_view(), name='index'),
    url(r'^order/(?P<pk>([0-9]+))/$', MenuPositionInOrderListView.as_view(), name='order'),
    url(r'^new_position/$', NewMenuPositionView.as_view(), name='add_position'),
    url(r'^menu_position/(?P<pk>([0-9]+))/$', MenuPositionDetailView.as_view(), name='menu_position'),

    url(r'^api-token-auth/', CustomObtainAuthToken.as_view(), name='auth'),

    url(r'^api_menu_positions/$', MenuPositionList.as_view(), name='api_menu_positions'),
    url(r'^api_menu_position/(?P<pk>([0-9]+))/$', MenuPositionDetail.as_view(), name='api_menu_position'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)