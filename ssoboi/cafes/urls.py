from django.conf.urls import url
from .views import get_cafe_by_coord,\
    get_item_by_id, get_cafe_by_name, CafeList, CafeDetail

urlpatterns = [
    url(r'^cafes/$', CafeList.as_view()),
    url(r'^cafes/(?P<pk>[0-9]+)/$', CafeDetail.as_view()),
    url(r'^cafes/get_cafe_by_name', get_cafe_by_name),
    url(r'^cafes/get_cafe_by_coord', get_cafe_by_coord),
    url(r'^get_item_by_id', get_item_by_id),
]
