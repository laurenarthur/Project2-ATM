from django.urls import path
#from django.conf.urls import  url
from . import views

urlpatterns = [
     path('', views.home, name='login'),
     path('login',views.home, name='login'),
     path('bankaccount',views.mainmenu, name='bankaccount'),
     path('balance',views.BalanceView, name='balance'),
     path('withdraw/', views.WithdrawView, name='withdraw'),
     path('transfer', views.TransferView, name='transfer'),
     path('changePhone',views.changePhone, name='changephone'),
     path('checkCode',views.checkCode,name='checkcode'),
     path('codeSent',views.codeSent,name='codesent'),
     path('pinChange',views.pinChange, name= 'pinchange'),


]
