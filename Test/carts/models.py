from django.db import models
from core.models import UserProfile

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey('core.UserProfile', related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey('core.UserProfile', related_name='seller', on_delete=models.CASCADE)
    product = models.ForeignKey('items.Items', on_delete=models.CASCADE, related_name='product')  # Assuming 'Item' is a model in your database
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_price(self):
        return self.product.price * self.quantity
   
    def __str__(self):
            return f"Order {self.id} - {self.product.name} x{self.quantity}"

   

class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    buyer = models.ForeignKey('core.UserProfile', related_name='payment_buyer', on_delete=models.CASCADE, default=1)  # Replace '1' with an appropriate default user ID
    seller = models.ForeignKey('core.UserProfile', related_name='payment_seller', on_delete=models.CASCADE,default=1)
    product = models.ForeignKey('items.Items', on_delete=models.CASCADE, related_name='payment_product',default=1)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    order_id = models.IntegerField(default=0)  # Default value to populate existing rows
   
    def process_payment(self):
        # Simulate payment processing logic
        if self.total_price <= self.buyer.balance:
            self.buyer.balance -= self.total_price
            self.buyer.save()
            self.seller.balance += self.total_price
            self.seller.save()
            
            # Create a new item for the buyer
            product1 = self.product
            # Check if the buyer already owns the product
            existing_item = product1.__class__.objects.filter(
                category=product1.category,
                name=product1.name,
                owned_by=self.buyer,
                for_sale=False
            ).first()

            if existing_item:
                # If the product already exists, increase its quantity
                existing_item.quantity += self.quantity
                existing_item.save()
                new_item = existing_item
            else:
                # Otherwise, create a new item for the buyer
                new_item = product1.__class__.objects.create(
                    category=product1.category,
                    name=product1.name,  # Add unique ID to the name
                    price=product1.price,
                    description=product1.description,
                    image=product1.image,
                    Available_Stock=True,
                    owned_by=self.buyer,
                    created_at=product1.created_at,
                    quantity=self.quantity,
                    for_sale=False,  # Assuming the item is no longer for sale after purchase
                    # Add any other fields that need to be copied
                )
            self.product = new_item
            self.save()
            # Update the original product's quantity
            product1.quantity -= self.quantity
            product1.save()
            
            # Delete the order
            Order.objects.filter(id=self.order_id).delete()
            
            # Mark the payment as successful
            self.is_successful = True
            self.save()
            return True
        return False

    def __str__(self):
        return f"Payment for {self.product.name} x{self.quantity} - {'Successful' if self.is_successful else 'Failed'}"
