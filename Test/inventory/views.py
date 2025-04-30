from django.shortcuts import render
from core.models import UserProfile
from items.models import Items

def account_page(request):
    user_profile = None
    available_items = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            available_items = Items.objects.filter(owned_by=user_profile)
            
        except UserProfile.DoesNotExist:
            user_profile = None
            available_items = None

    return render(request, 'inventory/inventory.html', {'available_items': available_items})
def item_detail(request, id):
    product = Items.objects.get(id=id)
    return render(request, 'inventory/item_detail.html', {'product': product})
