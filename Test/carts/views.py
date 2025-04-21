from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order
from items.models import Items

@login_required(login_url='login')  # Make sure to set this to your actual login URL name
def add_to_cart(request):
    if request.method == "GET":
        product_id = request.GET.get("product_id")
        quantity = int(request.GET.get("quantity", 1))
        product = get_object_or_404(Items, id=product_id)

        if quantity > product.quantity:
            messages.error(request, "Requested quantity exceeds available stock.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Create or update the order
        order, created = Order.objects.get_or_create(
            buyer=request.user,
            product=product,
            defaults={"quantity": quantity, "seller": product.owned_by},
        )

        if not created:
            if order.quantity + quantity > product.quantity:
                messages.error(request, "Requested quantity exceeds available stock.")
            else:
                order.quantity += quantity
                order.save()
                messages.success(request, "Item added to cart successfully!")
        else:
            messages.success(request, "Item added to cart successfully!")

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def index(request):
    orders = Order.objects.filter(buyer=request.user)
    total_price = sum(order.total_price for order in orders)
    return render(request, 'carts/cart.html', {'orders': orders, 'total_price': total_price})


@login_required(login_url='login')
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))

        if new_quantity > order.product.quantity:
            messages.error(request, "Requested quantity exceeds available stock.")
        else:
            order.quantity = new_quantity
            order.save()
            messages.success(request, "Order updated successfully!")

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    order.delete()
    messages.success(request, "Order removed successfully!")
    return redirect(request.META.get('HTTP_REFERER', '/'))
