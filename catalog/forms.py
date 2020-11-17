from django import forms
from catalog.models import ATMCard, Account, Machine, userActivity
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
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

class withdrawalForm(forms.Form):
    withdrawalBalance= forms.IntegerField(label="Withdrawal Amount",required=True)

    def clean_withdrawalBalance (self,*args,**kwargs):
        withdrawalBalance = self.cleaned_data.get('withdrawalBalance')

        ATM_Machine = Machine.objects.filter(pk=1)


        #Make sure they didn't input a negative or 0 amount
        if withdrawalBalance <= 0 :
            raise forms.ValidationError("Invalid.")
        #get first object in the user's activity model
        getUserPin = userActivity.objects.last()

        pin=getUserPin.returnpin()
        getATMObject =ATMCard.objects.filter(PIN=pin)
        AccountNum=Account.objects.filter(AccountNumber=(getATMObject[0].AccountNum))

        #Check if user has enough in bank to withdrawal this amount
        if(withdrawalBalance > int(AccountNum[0].AccBalance)):
            raise forms.ValidationError("Insufficient funds.")
        if(withdrawalBalance>ATM_Machine[0].currentBalance):
            raise forms.ValidationError("ATM too low")

        return withdrawalBalance

class TransferForm(forms.Form):

    amount_transfer = forms.IntegerField(label="Transfer Amount", required=True)
    receiver = forms.ModelChoiceField(queryset=Account.objects.all(), required=True)

    #Prevent Self Transfer
    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        getUserPin = userActivity.objects.last()
        pin = getUserPin.returnpin()
        getATMObject =ATMCard.objects.filter(PIN=pin)
        self.fields['receiver'].queryset = Account.objects.exclude(AccountNumber=(getATMObject[0].AccountNum))
        self.redirect = False

    def clean_amount_transfer(self,*args,**kwargs):

        amount = self.cleaned_data.get("amount_transfer")
        ATM_Machine = Machine.objects.filter(pk=1)




        if(amount<=0):
            raise forms.ValidationError("Cannot be less than 1")
        if(amount>ATM_Machine[0].currentBalance):
            raise forms.ValidationError("Insufficient funds.")

        getUserPin = userActivity.objects.last()

        pin=getUserPin.returnpin()
        getATMObject =ATMCard.objects.filter(PIN=pin)
        AccountNum=Account.objects.filter(AccountNumber=(getATMObject[0].AccountNum))

        if(AccountNum[0].AccBalance < amount):
            raise forms.ValidationError("Insufficient funds.")
        return amount

class phoneForm(forms.Form):
    #Enter new phone number prompt
    AccountNumber = forms.CharField(max_length=10, label="Account Number", required=True)

    newPhoneNumber = forms.IntegerField(label="New Phone Number", required=True)

    #Code
    def clean_AccountNumber(self,*args, **kwargs):
        new_AccountNumber = self.cleaned_data.get("AccountNumber")

        if not Account.objects.filter(AccountNumber=new_AccountNumber).exists():
            raise forms.ValidationError("Not a valid account")

        return new_AccountNumber

        def clean_newPhoneNumber(self, *args,**kwargs):
            new_newPhoneNumber = self.cleaned_data.get("newPhoneNumber")

            if(new_newPhoneNumber < 1000000000 or new_newPhoneNumber > 9999999999):
                raise forms.ValidationError("Number needs to be 10 digits")
            return new_newPhoneNumber

class checkCodeForm(forms.Form):
    passCode = forms.IntegerField(label = "Pass Code", required=True)

    def clean_passCode(self, *args,**kwargs):
        new_passCode = self.cleaned_data.get("passCode")

        if(new_passCode != 1111111122222222222):
            raise forms.ValidationError("Incorrect Code")
        return new_passCode

class newPinForm(forms.Form):
    old_pin = forms.IntegerField(label="Old Pin", required=True)
    new_pin = forms.IntegerField(label="New Pin", required=True)

    def clean_old_pin (self, *args, **kwargs):
        old_entered = self.cleaned_data.get("old_pin")
        if old_entered <=999 or old_entered >= 10000:
            raise forms.ValidationError("Not a valid pin")
        if not ATMCard.objects.filter(PIN=old_entered).exists():
            raise forms.ValidationError("Not a valid pin.")
        Card=ATMCard.objects.filter(PIN=old_entered)
        if Card[0].expired_recently():
            raise forms.ValidationError("Not a pin")
        if old_entered != userActivity.objects.last().returnpin():
            raise forms.ValidationError("Unauthorized")

        return old_entered

    def clean_new_pin (self,*args,**kwargs):
        new_pin=self.cleaned_data.get("new_pin")
        if new_pin <=999 or new_pin >=10000:
            raise forms.ValidationError("Not a valid pin.")
        if ATMCard.objects.filter(PIN=new_pin).exists():
            raise forms.ValidationError("Pin already in use.")
        return new_pin
