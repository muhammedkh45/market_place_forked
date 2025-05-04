# Create your models here.
from django.db import models


class APIClient(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    user_profile = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='api_clients', default=1)

    def __str__(self):
        return self.name



