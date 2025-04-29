from django.shortcuts import render
from core.models import UserProfile

def account_page(request):
    user_profile = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    return render(request, 'inventory.html', {'profile': user_profile})
