from django import forms
from catalog.models import ATMCard, Account, Machine
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
    amount = forms.IntegerField(min_value=1)
    account = forms.IntegerField()
    atm = forms.IntegerField()
