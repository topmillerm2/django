from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^verify$', views.verify),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add_trip),
    url(r'^process/trip$', views.process),
    url(r'^destination/(?P<number>\d+)$', views.destination_page),
    url(r'^logout$', views.logout),

]