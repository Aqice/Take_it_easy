from .views import UserReg, UserAuth, UserlLogOut

from django.conf.urls import url


urlpatterns = [
    url(r'^reg', UserReg.as_view()),
    url(r'^auth', UserAuth.as_view()),
    url(r'^logout', UserlLogOut.as_view()),
]
