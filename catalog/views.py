from django.shortcuts import render
from catalog.models import ATMCard, Account, Machine, userActivity
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from catalog.forms import HomeForm

# Create your views here.

def base(request):
    return render(request, 'atm/base.html')
def home(request):
    if request.method=="POST":
        form=HomeForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']

            #if pin exits add to user activity database that holds the users current pin
            if ATMCard.objects.filter(PIN=pin).exists():
                pinEntered=userActivity(pin=pin)
                pinEntered.save()


                UsersATMCard=ATMCard.objects.filter(PIN=pin)

                contents={
                "userName": UsersATMCard[0].name,
                "AccountNumber": UsersATMCard[0].AccountNum

                }


                #redirect to allow user to choose what do to their bank account
                return render(request,'atm/bankaccount.html',contents)

        #form not valid return to login screen with validation error raised
        else:
            ctx={"form":form}
            return render(request,'atm/login.html',ctx)
    form=HomeForm()
    return render (request, 'atm/login.html',{'form': form})
    
def mainmenu(request):
    getPin = userActivity.objects.last().returnpin()
    UsersATMCard=ATMCard.objects.filter(PIN=getPin)
    name= UsersATMCard[0].name
    account= UsersATMCard[0].AccountNum
    contents={
    "userName": name,
    "AccountNumber": account,

    }
    return render(request,'atm/bankaccount.html',contents)