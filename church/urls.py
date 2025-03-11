from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('sermons/', views.sermon_list, name='sermon_list'),
    path('contact/', views.contact, name='contact'),
   
]