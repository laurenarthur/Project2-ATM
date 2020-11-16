from django.shortcuts import render,redirect
from catalog.models import ATMCard, Account, Machine, userActivity, updatePhone
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from catalog.forms import HomeForm, WithdrawForm, TransferForm,phoneForm,checkCodeForm,newPinForm

# Create your views here.

def base(request):
    return render(request, 'atm/login.html')

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


def BalanceView(request):
    #Pin for identity
    getPinObject = userActivity.objects.last();
    getUserpin = getPinObject.returnpin()

    #get Pin from ATMCard model
    getATMPIN =ATMCard.objects.filter(PIN=getUserpin)

    #Get Account Number
    accountNumber=Account.objects.filter(AccountNumber=(getATMPIN[0].AccountNum))

    #Clean input
    account=accountNumber.values_list('AccountNumber')[0][0]

    balance = accountNumber[0].AccBalance
    contents={
    "AccountNumber": account,
    "AccBalance": balance
    }
    return render(request,'atm/balance.html', contents)

def WithdrawView(request):
    if request.method == "POST":
        form = WithdrawForm(request.POST)

        if form.is_valid():
            userAmount = form.cleaned_data['amount']

            getPinObject = userActivity.objects.last();
            getUserpin = getPinObject.returnpin()

            #get Pin from ATMCard model
            getATMPIN =ATMCard.objects.filter(PIN=getUserpin)

            #Get Account Number
            accountNumber=Account.objects.filter(AccountNumber=(getATMPIN[0].AccountNum))

            #Get balance
            balance=accountNumber[0].AccBalance

            #compute new balance
            newBalance =  balance-userAmount
            ATMMachineFind=Machine.objects.filter(pk=1)
            ATMAmount=ATMMachineFind[0].currentBalance
            ATMMachineFind.update(currentBalance=(ATMAmount-userAmount))

            #set new balance to newAccount
            Account.objects.filter(AccountNumber=(accountNumber[0].AccountNumber)).update(AccBalance=newBalance)

            #create dictionary with user's new account after withdrawal
            contents={
            'balance':  accountNumber[0].AccBalance,
            'PreviousAmount': balance,
            'amountwithdrawan': userAmount,
                }
            #send dictionary with confirmation page
            return render(request,'atm/confirmationform.html',contents)

        else:
            #dictionary with current page
            ctx={"form":form}

            #send page again with validation errors
            return render(request,'atm/withdraw.html',ctx)

    form=WithdrawForm()

    return render(request, "atm/withdraw.html", {'form': form})

def TransferView(request):
    if request.method == "POST":
        form = TransferForm(request.POST)

        if form.is_valid():
            userAmount = form.cleaned_data['amount']

            getPinObject = userActivity.objects.last();
            getUserpin = getPinObject.returnpin()

            #get Pin from ATMCard model
            getATMPIN =ATMCard.objects.filter(PIN=getUserpin)

            #Get Account Number
            accountNumber=Account.objects.filter(AccountNumber=(getATMPIN[0].AccountNum))
            accountNumber2=Account.objects.filter(AccountNumber=form.cleaned_data['receiver'])

            #Self Transfer
            if accountNumber is accountNumber2:
                userAmount = '0'

            #Get balance
            balance=accountNumber[0].AccBalance
            balance2=accountNumber2[0].AccBalance

            #compute new balance
            newBalance =  balance-userAmount
            newBalance2 = balance2+userAmount


            #set new balance to newAccount
            Account.objects.filter(AccountNumber=(accountNumber[0].AccountNumber)).update(AccBalance=newBalance)
            Account.objects.filter(AccountNumber=(accountNumber2[0].AccountNumber)).update(AccBalance=newBalance2)

            #Clean Output
            user2=accountNumber2.values_list('userName')[0][0]




            #create dictionary with user's new account after transfer
            contents={
            'account1': accountNumber,
            'account2': accountNumber2,
            'balance':  accountNumber[0].AccBalance,
            'PreviousAmount': balance,
            'amountTransferred': userAmount,
            'receiver': user2,
            'receiverBalance': newBalance2
                }
            #send dictionary with confirmation page
            return render(request,'atm/confirmationform2.html',contents)

        else:
            #dictionary with current page
            ctx={"form":form}

            #send page again with validation errors
            return render(request,'atm/transfer.html',ctx)

    form=TransferForm()

    return render(request, "atm/transfer.html", {'form': form})

#Function that changes phone Number
def changePhone(request):
    if request.method=="POST":
        form = phoneForm(request.POST)

        if form.is_valid():
            #Sends correct info to page
            new_newPhoneNumber = form.cleaned_data['newPhoneNumber']
            new_AccountNumber = form.cleaned_data['AccountNumber']

            userInput = updatePhone(AccountNum = new_AccountNumber, newNumber = new_newPhoneNumber)
            userInput.save()

            return render(request, 'atm/codeSent.html')

        else:
            #incorrect inputs keeps user on this page
            ctx={"form":form}

            return render(request, 'atm/changePhone.html', {'form':form})
    form=phoneForm()
    return render (request, 'atm/changePhone.html',{'form': form})

def checkCode(request):
    if request.method=="POST":
        form=checkCodeForm(request.POST)
        if form.is_valid():
            #we would update phone Number
            new_passCode = form.cleaned_data['passCode']
            #account number to be changed
            acctToChange= updatePhone.objects.last()
            #find account based on this Number
            temp =acctToChange.AccountNum
            compare = Account.objects.filter(AccountNumber= temp)
            #replace old phone with new phone
            Nphone = acctToChange.newNumber
            compare.update(phoneNumber=Nphone)

            return render(request,'atm/sucess.html')
        else:
            #incorrect keeps at this page
            ctx={"form":form}
            return render(request,'atm/checkCode.html',ctx)

    form=checkCodeForm()
    return render(request,'atm/checkCode.html',{'form': form})

def codeSent(request):
     return render(request,'atm/codeSent.html')

def pinChange(request):

    if request.method=="POST":

        form=newPinForm(request.POST)
        if form.is_valid():

            old_pin = form.cleaned_data['old_pin']
            new_pin = form.cleaned_data['new_pin']


            #redirect to allow user to choose what do to their bank account
            card =ATMCard.objects.filter(PIN=old_pin)
            print(card)
            card.update(PIN=new_pin)


            return render(request,'atm/confirmationPin.html')

        #form not valid return to login screen with validation error raised
        else:

            ctx={"form":form}
            return render(request,'atm/changePinInformation.html',ctx)
    form=newPinForm()
    return render(request,'atm/changePinInformation.html',{'form':form})
