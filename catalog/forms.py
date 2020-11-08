from django import forms
from catalog.models import ATMCard, Account, Machine, userActivity
from django.core.exceptions import ValidationError
import random

class HomeForm(forms.Form):
    pin = forms.IntegerField(label="Pin",required=True)
    def clean_pin (self,*args,**kwargs):
        pinentered  = self.cleaned_data.get("pin")
        if pinentered <=999 or pinentered >=10000:
            raise forms.ValidationError("Invalid user credentials.")
        if not ATMCard.objects.filter(PIN=pinentered).exists():
            raise forms.ValidationError("Invalid user credentials.")
        Card=ATMCard.objects.filter(PIN=pinentered)
        if Card[0].expired_recently():
            raise forms.ValidationError("Expired.")

        #if ATMCard.objects.filter(PIN=pinentered).is
        return pinentered

class WithdrawForm(forms.Form):

    amount = forms.IntegerField(label="Withdrawal Amount", required=True)
    
    def clean_withdrawBalance (self, *args, **kwargs):
        amount = self.cleaned_data.get('amount')
        
        ATMMachine = Machine.objects.filter(pk=1)
        
        #Check if they entered negative or zero amount
        if amount <= 0 :
            raise forms.ValidationError("Invalid")
        getUserPin = userActivity.objects.last()
        
        pin = getUserPin.returnpin()
        getATMObject =ATMCard.objects.filter(PIN=pin)
        AccountNum=Account.objects.filter(AccountNumber=(getATMObject[0].AccountNum))
        
        #Check if user has enough in bank to withdrawal this amount
        if(amount > int(AccountNum[0].AccBalance)):
            raise forms.ValidationError("Insufficient funds.")
        if(amount>ATMMachine[0].currentBalance):
            raise forms.ValidationError("ATM too low")

        return amount
