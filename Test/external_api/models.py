# Create your models here.
from django.db import models
from items.models import Items
from core.models import UserProfile

class APIClient(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    user_profile = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='api_clients', default=1)

    def __str__(self):
        return self.name

# marketplace/models.py
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} created at {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} - {self.quantity} units"

