from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Order
from items.models import Items  # Assuming Items is the product model

def add_to_cart(request):
    if request.method == "GET":
        product_id = request.GET.get("product_id")
        quantity = int(request.GET.get("quantity", 1))
        product = get_object_or_404(Items, id=product_id)
        # Check if the requested quantity is available
       
        # Create or update the order
        order, created = Order.objects.get_or_create(
            buyer=request.user,
            product=product,
            defaults={"quantity": quantity, "seller": product.owned_by},
        )
        # Decrease the product quantity
        
        if not created:
            if order.quantity + quantity > product.quantity:
              messages.error(request, "Requested quantity exceeds available stock.")
              return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.success(request, "Item added to cart successfully!")
                redirect(request.META.get('HTTP_REFERER', '/'))
            order.quantity += quantity
            order.save()
        else:
            messages.success(request, "Item added to cart successfully!")
           
    return redirect(request.META.get('HTTP_REFERER', '/'))

def index(request):
    orders = Order.objects.filter(buyer=request.user)  # Filter orders by the logged-in user
    total_price = sum(order.total_price for order in orders)  # Calculate total price
    return render(request, 'carts/cart.html', {'orders': orders, 'total_price': total_price})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)  # Ensure the order belongs to the logged-in user

    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))

        # Check if the new quantity is valid
        if new_quantity > order.product.quantity:
            messages.error(request, "Requested quantity exceeds available stock.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Update the order quantity
        order.quantity = new_quantity
        order.save()

        messages.success(request, "Order updated successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # If the request is not POST, redirect to the cart
    return redirect(request.META.get('HTTP_REFERER', '/'))

def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)  # Ensure the order belongs to the logged-in user
    # Delete the order
    order.delete()

    messages.success(request, "Order removed successfully!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

