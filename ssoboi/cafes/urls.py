from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import add_cafe, get_cafe_by_id, remove_cafe, get_cafe_by_coord, get_coord_by_id, \
    get_cafe_opening_hours_by_id, get_owner_by_id, get_item_by_id, get_all_cafes, get_cafe_by_name

urlpatterns = [
    url(r'^cafes/$', get_all_cafes),
    url(r'^cafes/(?P<pk>[0-9]+)/$', get_cafe_by_id),
    url(r'^add_cafe', add_cafe),
    url(r'^remove_cafe', remove_cafe),
    url(r'^cafes/get_cafe_by_coord', get_cafe_by_coord),
    url(r'^get_coord_by_id', get_coord_by_id),
    url(r'^get_cafe_opening_hours_by_id', get_cafe_opening_hours_by_id),
    url(r'^get_owner_by_id', get_owner_by_id),
    url(r'^get_item_by_id', get_item_by_id),
]
