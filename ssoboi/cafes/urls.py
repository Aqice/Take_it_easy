from django.conf.urls import url
from .views import get_cafe_by_coord
from .views import get_item_by_id
from .views import get_cafe_by_name
from .views import CafeList
from .views import CafeDetail
from .views import OrderCreation
from .views import OrdersList
from .views import ChangingOrderStatus

urlpatterns = [
    url(r'^cafes/$', CafeList.as_view()),
    url(r'^cafes/(?P<pk>[0-9]+)/$', CafeDetail.as_view()),
    url(r'^cafes/get_cafe_by_name', get_cafe_by_name),
    url(r'^cafes/get_cafe_by_coord', get_cafe_by_coord),
    url(r'^cafes/get_item_by_id', get_item_by_id),
    url(r'^cafes/create_order', OrderCreation.as_view()),
    url(r'^cafes/get_orders', OrdersList.as_view()),
    url(r'^cafes/change_order_status', ChangingOrderStatus.as_view()),
]
