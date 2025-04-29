
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        app_label = 'inventory'

class Item(models.Model):
    STATUS_CHOICES = (
        ('purchased', 'Purchased'),
        ('sold', 'Sold'),
        ('available', 'Available'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
