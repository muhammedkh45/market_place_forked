from django.db import models
from core.models import UserProfile
from items.models import Items

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('transaction', 'Transaction'),
        ('deposit', 'Deposit'),
    )

    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(UserProfile, related_name='transactions_bought', on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(UserProfile, related_name='transactions_sold', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='transaction')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
