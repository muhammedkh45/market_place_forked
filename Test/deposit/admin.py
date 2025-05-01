from django.contrib import admin
from .models import   PaymentCard, Deposit
# Register your models here.

admin.site.register(PaymentCard)
admin.site.register(Deposit)