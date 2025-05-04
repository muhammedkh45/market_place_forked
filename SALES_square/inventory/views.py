from django.shortcuts import render,redirect
from core.models import UserProfile
from items.models import Items,Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .forms import ItemForm
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from items.models import Items  # Make sure this import exists


@login_required(login_url='login')
def account_page(request):
    user_profile = None
    available_items = None
    categories = Category.objects.all()
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            available_items = Items.objects.filter(owned_by=user_profile).order_by('-created_at')
            
        except UserProfile.DoesNotExist:
            user_profile = None
            available_items = None

    return render(request, 'inventory/inventory.html', {'available_items': available_items,'categories': categories})
@login_required(login_url='login')
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
                quantity_advertise = form.cleaned_data.get('quantity_advertise')
                if item.advertise and quantity_advertise > item.quantity:
                    form.add_error('quantity', "Quantity to advertise cannot exceed the total quantity.")
                    return render(request, 'inventory/edit_item.html', {'form': form, 'title': 'Edit Item', 'item': item})
                else:
                    saved_item = form.save()
                    messages.success(request, 'Item updated successfully!')
                    return redirect('item_detail', id=saved_item.id)
        else:
            form = ItemForm(instance=item)

        return render(request, 'inventory/edit_item.html', {'form': form, 'title': 'Edit Item', 'item': item})

@login_required(login_url='login')
def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Items, id=item_id)
        item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('Inventory')  # Make sure 'inventory' is the correct URL name
    # If not POST, redirect back to inventory
    return redirect('Inventory')


@login_required
def add_item(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add items.")
        return redirect('login')  
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category_name = request.POST.get('category')  
            price_str = request.POST.get('price')
            quantity_str = request.POST.get('quantity', '1')  # default to 1 if missing

            try:
                price = float(price_str)
                quantity = int(quantity_str)
            except ValueError:
                messages.error(request, "Price must be a number and quantity must be an integer.")
                return redirect('add_item')
            # Convert to Decimal first
            # price = Decimal(price) if price else None
            # if not price or price <= 0:  # Proper numerical comparison
            #     messages.error(request, "Please enter a valid positive price")
            #     return redirect('add_item')
            
            description = request.POST.get('description')
            image = request.FILES.get('image')
            # quantity = request.POST.get('quantity')  # Default to 1 if not provided
            

            # Validate image
            if not image:
                messages.error(request, "Please upload an image for the item.")
                return redirect('add_item')

            # Validate required fields
            if not all([name, category_name, price]):  
                messages.error(request, "Please fill all required fields.")
                return redirect('add_item')
            
            # Get or create the category by name
            category, created = Category.objects.get_or_create(name=category_name)
            
            # Create and save the new item
            Items.objects.create(
                name=name,
                category=category,  # Now using the category object directly
                price=price,
                description=description,
                image=image,
                quantity=quantity,  # Default quantity set to 1
                owned_by=UserProfile.get_profile_by_user(request.user)  # Assuming you have a method to get the user profile, 
            )
            
            messages.success(request, "Item added successfully!")
            return redirect('Inventory')
            
        except Exception as e:
            messages.error(request, f"Error adding item: {str(e)}")
            return redirect('add_item')
    
    # GET request - show the form
    return render(request, 'inventory/add_item.html', {'categories': Category.objects.all()})



@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category, created = Category.objects.get_or_create(name=name.strip())
            if created:
                messages.success(request, f"Category '{category.name}' added successfully!")
            else:
                messages.info(request, "Category already exists.")
        else:
            messages.error(request, "Category name cannot be empty.")
    return redirect('Inventory')


@login_required
def remove_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            
            #Check if category is being used by any items
            if category.items.exists():  # Assuming you have a related_name='items' on your Item model
                messages.error(request, f"Cannot delete '{category.name}' - it contains items!")
                return redirect('Inventory')  # Or your inventory page name
            
            category.delete()
            messages.success(request, f"Category '{category.name}' deleted successfully!")
        except Category.DoesNotExist:
            messages.error(request, "Category not found!")
        
        return redirect('Inventory')  # Redirect back to inventory page
    
    # If not POST, redirect somewhere safe
    return redirect('Inventory')