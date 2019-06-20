from django.conf.urls import url
from recog_entities import views

urlpatterns = [
    url(r'^$', views.loadindex, name='home'),
    url(r'^rdf', views.identificador, name='lee'),
    url(r'^about', views.info, name='info'),
]