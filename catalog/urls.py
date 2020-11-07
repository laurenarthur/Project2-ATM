from django.urls import path
from . import views

urlpatterns = [
     path('', views.base, name='base'),
     path('login',views.home, name='home'),
     path('bankaccount',views.mainmenu, name='bankaccount'),
     path('balance',views.BalanceView, name='balance'),
     path('withdraw', views.WithdrawView, name='withdraw'),


]
