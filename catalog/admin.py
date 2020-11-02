from django.contrib import admin

# Register your models here.
from .models import Account, Machine, ATMCard
##
admin.site.site_header = "Administration"
admin.site.register(ATMCard)
admin.site.register(Account)
admin.site.register(Machine)
##admin.site.register(Refill)
