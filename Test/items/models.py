from django.db import models
from django.contrib.auth.models import User
from core.models import UserProfile

class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Items(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/%y/%m/%d',default='default-product-image.jpg', blank=True)
    Available_Stock = models.BooleanField(default=True)
    owned_by = models.ForeignKey('core.UserProfile', related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    for_sale = models.BooleanField(default=True)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )
    


    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Items'

    def save(self, *args, **kwargs):
        # Automatically update 'Available Stock' based on 'quantity'
        self.Available_Stock = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name