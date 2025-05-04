from django.db import models
from django.contrib.auth.models import User
from core.models import UserProfile





class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # For example, store amounts in dollars
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return f"Deposit {self.transaction_id} - {self.status}"