from django.conf.urls import url
from .views import CafeCoordinates
from .views import ItemDetail
from .views import CafeName
from .views import CafeList
from .views import CafeDetail
from .views import OrderCreation
from .views import OrdersList
from .views import ChangingOrderStatus

urlpatterns = [
    url(r'^cafes/$', CafeList.as_view()),
    url(r'^cafes/(?P<pk>[0-9]+)/$', CafeDetail.as_view()),
    url(r'^cafes/get_cafe_by_name', CafeName.as_view()),
    url(r'^cafes/get_cafe_by_coord', CafeCoordinates.as_view()),
    url(r'^cafes/get_item_by_id', ItemDetail.as_view()),
    url(r'^cafes/create_order', OrderCreation.as_view()),
    url(r'^cafes/get_orders', OrdersList.as_view()),
    url(r'^cafes/change_order_status', ChangingOrderStatus.as_view()),
]
