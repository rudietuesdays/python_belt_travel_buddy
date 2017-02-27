#### TRAVEL DASHBOARD URLS ####
from django.conf.urls import url
from . import views

app_name = 'travelDash'

urlpatterns = [
    url(r'^dashboard$', views.index, name ='dashboard'),
    url(r'^add_plan$', views.add_plan_page, name ='add_plan'),
    url(r'^add$', views.add_plan, name ='add'),
    url(r'^destination/(?P<id>\d+)$', views.view_destination, name ='destination'),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip, name ='join_trip'),

]
