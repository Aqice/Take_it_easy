from django.conf.urls import url

from .views import add_cafe

urlpatterns = [
    url(r'^add_cafe', add_cafe, name='index'),
]
