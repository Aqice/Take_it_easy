from django.conf.urls import url
from .views import get_cafe_by_id, get_cafe_by_coord, \
    get_owner_by_id, get_item_by_id, CafesList, get_cafe_by_name

urlpatterns = [
    url(r'^cafes/$', ),
    url(r'^cafes/(?P<pk>[0-9]+)/$', get_cafe_by_id),
    url(r'^cafes/get_by_name', get_cafe_by_name),
    url(r'^cafes/get_cafe_by_coord', get_cafe_by_coord),
    url(r'^get_owner_by_id', get_owner_by_id),
    url(r'^get_item_by_id', get_item_by_id),
]
