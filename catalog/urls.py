from django.urls import path
from . import views

urlpatterns = [
     path('', views.base, name='base'),
     path('login',views.home, name='home'),

]
