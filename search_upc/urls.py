from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^(?P<upc>[a-z0-9]+)$', views.searchUpcRequest),
    #url(r'^$', views.searchUpcRequest),
]
