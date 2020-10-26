from django.test import TestCase
from django.urls import reverse
from atm.models import Card, Account,Machine
import datetime
# Create your tests here.
class AccountTest(TestCase):

    def create_account(self, AccountNumber="1009",nameAcc="Jeffrey Smith",phoneNumber="2704561234",balance=100):
        return Account.objects.create(AccountNumber=AccountNumber, nameAcc=nameAcc,phoneNumber=phoneNumber,balance=balance)

    def test_account_creation(self):
        w = self.create_account()
        self.assertEqual(w.AccountNumber,"1009")

    def test_account_string(self):
        w=self.create_account()
        self.assertEqual(w.__str__(),"1009")

class ATMCardTest(TestCase):

    def create_atmcard(self, ATMCardNumber="8888888",PIN=1234, name="Danzel Washington", DOI=datetime.date.today(), ExpirationDate=datetime.date.today()+datetime.timedelta(days=30),Address="123 Street"):
        w_=Account.objects.create(AccountNumber="1009", nameAcc="Jeffrey Smith",phoneNumber="2704561234",balance=100)
        return ATMCard.objects.create(ATMCardNumber=ATMCardNumber, AccountNum=w_ ,PIN=PIN, name=name, DOI=DOI, ExpirationDate=ExpirationDate,Address=Address)

    def test_atm_creation(self):
        w=self.create_atmcard()
        self.assertEqual(w.ATMCardNumber,"8888888")

    def test_atm_string(self):
        w=self.create_atmcard()
        self.assertEqual(w.__str__(),"8888888 - Danzel Washington")

    def test_expired_recently(self):
        w=self.create_atmcard()
        self.assertEqual(w.expired_recently(),False)

    def test_expired_recently_(self):
        w=self.create_atmcard()
        w.ExpirationDate=datetime.date.today()-datetime.timedelta(days=30)
        self.assertEqual(w.expired_recently(),True)

    def test_accoutReturn(self):
        w=self.create_atmcard()
        self.assertEqual(w.accoutReturn(), "8888888")






class ATMMachineTest(TestCase):
    def create_atmmachine(self,UID=7890,currentBalance=200,location="Georgia",status=False,lastFill=datetime.date.today(),nextMain=datetime.date.today(),previousBalance=100 ):
        return ATMMachine.objects.create(UID=UID,currentBalance=currentBalance,location=location,status=status,lastFill=lastFill,nextMain=nextMain,previousBalance=previousBalance)

    def test_atmmachine_creation(self):
        w=self.create_atmmachine()
        self.assertEqual(w.UID,7890)

    def test_atmmachine_string(self):
        w = self.create_atmmachine()
        self.assertEqual(w.__str__(),"ATM - 7890")

