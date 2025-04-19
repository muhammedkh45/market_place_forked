from django.db import models

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey('auth.User', related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey('auth.User', related_name='seller', on_delete=models.CASCADE)
    product = models.ForeignKey('items.Items', on_delete=models.CASCADE, related_name='product')  # Assuming 'Item' is a model in your database
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_price(self):
        return self.product.price * self.quantity
   
    def __str__(self):
            return f"Order {self.id} - {self.product.name} x{self.quantity}"

   
