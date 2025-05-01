from django.db import models
from django.contrib.auth.models import User
from core.models import UserProfile



class PaymentCard(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=False)
    card_number = models.CharField(max_length=16,null=False)
    holder_name = models.CharField(max_length=100,null=False)
    expiry_date = models.CharField(max_length=5,null=False)  # MM/YY format TODO : learn to check this format soon plllzzzz
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def masked_number(self):
        return f"**** **** **** {self.card_number[-4:]}"
    
    def __str__(self):
        return f"{self.user.user.username}'s card details"

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