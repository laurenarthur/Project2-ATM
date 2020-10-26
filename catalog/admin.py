from django.contrib import admin

# Register your models here.
from .models import Machine, Card
##
admin.site.site_header = "Administration"
admin.site.register(Card)
admin.site.register(Machine)
##admin.site.register(Refill)
