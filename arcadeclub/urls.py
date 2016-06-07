"""arcadeclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
# from django.conf.urls import url, include
# from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

from django.conf.urls import url, include
#from django.contrib.auth.models import User
from arcadeclub.models import Utente
from rest_framework import routers, serializers, viewsets
#from arcadeclub.views import utenti_list

# Serializers define the API representation.
class UtenteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utente
        fields = ('id', 'username', 'pwd', 'device')

# ViewSets define the view behavior.
class UtenteViewSet(viewsets.ModelViewSet):
    queryset = Utente.objects.all()
    serializer_class = UtenteSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'prova', UtenteViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

#from django.conf.urls import url
from arcadeclub import views


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^arcadeclub$', views.utenti_list),
    #url(r'^arcadeclub/(?P<id>[0-9]+)/$', views.utenti_detail),
    url(r'^arcadeclub/(?P<username>[a-z0-9]+)/(?P<pwd>[a-z0-9]+)/$', views.utenti_loginRequest),
    url(r'^arcadeclub/(?P<id_telefono>[a-z0-9]+)/immagine/(?P<image_file>[a-z_0-9]+)/', views.image),
    url(r'^arcadeclub/(?P<id_telefono>[a-z0-9]+)/magazzino', views.magazzino_detail),
    url(r'^arcadeclub/(?P<id_telefono>[a-z0-9]+)/venduti', views.venduti_detail),
    url(r'^arcadeclub/(?P<id_telefono>[a-z0-9]+)/search_upc', views.searchUpcRequest),
]

