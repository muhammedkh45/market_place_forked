from django.db import models
from core.models import UserProfile
from items.models import Items
from dashboard.models import Transaction

class Order(models.Model):
    buyer = models.ForeignKey(UserProfile, related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(UserProfile, related_name='seller', on_delete=models.CASCADE)
    product = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Order {self.id} - {self.product.name} x{self.quantity}"

class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    buyer = models.ForeignKey(UserProfile, related_name='payment_buyer', on_delete=models.CASCADE, default=1)
    seller = models.ForeignKey(UserProfile, related_name='payment_seller', on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='payment_product', default=1)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    order_id = models.IntegerField(default=0)

    def process_payment(self):
        if self.total_price <= self.buyer.balance:
            self.buyer.balance -= self.total_price
            self.buyer.save()
            self.seller.balance += self.total_price
            self.seller.save()

            product1 = self.product
            existing_item = product1.__class__.objects.filter(
                category=product1.category,
                name=product1.name,
                owned_by=self.buyer,
                for_sale=False
            ).first()

            if existing_item:
                existing_item.quantity += self.quantity
                existing_item.save()
                new_item = existing_item
            else:
                new_item = product1.__class__.objects.create(
                    category=product1.category,
                    name=product1.name,
                    price=product1.price,
                    description=product1.description,
                    image=product1.image,
                    Available_Stock=True,
                    owned_by=self.buyer,
                    created_at=product1.created_at,
                    quantity=self.quantity,
                    for_sale=False
                )

            self.product = new_item
            self.save()

            product1.quantity -= self.quantity
            product1.save()

            from dashboard.models import Transaction
            Transaction.objects.create(
                buyer=self.buyer,
                seller=self.seller,
                product=self.product,
                total_price=self.total_price,
                status='transaction'
            )

            Order.objects.filter(id=self.order_id).delete()

            self.is_successful = True
            self.save()
            return True
        return False

    def __str__(self):
        return f"Payment for {self.product.name} x{self.quantity} - {'Successful' if self.is_successful else 'Failed'}"
