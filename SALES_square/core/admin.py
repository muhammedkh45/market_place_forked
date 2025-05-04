from django.contrib import admin
from .models import ContactMessage
from .models import UserProfile, Review
admin.site.register(ContactMessage)
admin.site.register(UserProfile)
admin.site.register(Review)
# Register your models here.
