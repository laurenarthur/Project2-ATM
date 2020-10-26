from django.shortcuts import render
from catalog.models import Card, Account, Machine
from django.core.exceptions import ValidationError
from django.http import HttpResponse

# Create your views here.

def base(request):
    return render(request, 'atm/base.html')
