from django.db import models
from django.utils import timezone
import datetime
from django.db.models.signals import post_save

# Create your models here.

class Account(models.Model):
    AccountNumber = models.CharField(max_length=10)
    userName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=12)
    AccBalance = models.IntegerField(default=0)

    def __str__(self):
        return self.AccountNum

class Card(models.Model):
    ATMCardNumber=models.CharField(max_length=200)
    AccountNum=models.ForeignKey(Account,on_delete=models.CASCADE)
    PIN=models.IntegerField(default=0)
    name=models.CharField(max_length=200)
    DOI=models.DateField("Date Issued")
    ExpirationDate=models.DateField()
    Address=models.CharField(max_length=200)

    def __str__(self):
        return self.ATMCardNumber+ " - "+self.name

    def expired_recently(self):
        return self.ExpirationDate < datetime.date.today()
    def accoutReturn(self):
        return self.ATMCardNumber
    class Meta:
        verbose_name="ATM Card"

class Machine(models.Model):
    UID = models.IntegerField(default=0)
    currentBalance=models.IntegerField(default=0)
    location=models.CharField(max_length=200)
    status=models.BooleanField(default=False)
    lastFill=models.DateField("Date Issued: ")
    nextMain = models.DateField("Date Issued: ")
    previousBalance=models.IntegerField(default= 0)
    
    def __str__(self):
        return "ATM - "+str(self.UID)
    class Meta:
        verbose_name='ATM Machine'


##class Refill(models.Model):
##
##class userActivity(models.Model):
##
##class updatePhone(models.Model):
    
