from django.contrib import admin
from .models import UserBalance , PaymentCard, Deposit
# Register your models here.

admin.site.register(UserBalance)
admin.site.register(PaymentCard)
admin.site.register(Deposit)