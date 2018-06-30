from django.conf.urls import url

from .views import add_cafe, get_cafe_by_id, remove_cafe, get_cafe_by_coord

urlpatterns = [
    url(r'^add_cafe', add_cafe),
    url(r'^get_cafe_by_id', get_cafe_by_id),
    url(r'^remove_cafe', remove_cafe),
    url(r'^get_cafe_by_coord', get_cafe_by_coord)
]
