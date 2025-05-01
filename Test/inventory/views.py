from django.shortcuts import render
from core.models import UserProfile
from items.models import Items
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .forms import ItemForm
from django.contrib import messages

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

@login_required(login_url='login')
def edit_item(request, id):
        item = get_object_or_404(Items, id=id)

        if request.user != item.owned_by.user:
            messages.error(request, 'You do not have permission to edit this item.')
            return render(request, 'inventory/inventory.html', {'error': 'You do not have permission to edit this item.'})

        if request.method == 'POST':
            form = ItemForm(request.POST,request.FILES, instance=item)
            if form.is_valid():
                saved_item = form.save()
                messages.success(request, 'Item updated successfully!')
                return redirect('item_detail', id=saved_item.id)
        else:
            form = ItemForm(instance=item)

        return render(request, 'inventory/edit_item.html', {'form': form, 'title': 'Edit Item', 'item': item})

@login_required(login_url='login')
def delete_item(request, id):
    item = get_object_or_404(Items, id=id)

    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('Inventory')