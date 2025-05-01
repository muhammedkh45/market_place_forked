from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, Payment
from items.models import Items
from core.models import UserProfile

@login_required(login_url='login')
def add_to_cart(request):
    if request.method == "GET":
        product_id = request.GET.get("product_id")
        quantity = int(request.GET.get("quantity", 1))
        product = get_object_or_404(Items, id=product_id)

        if quantity > product.quantity:
            messages.error(request, "Requested quantity exceeds available stock.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        user_profile = UserProfile.get_profile_by_user(user=request.user)

        order, created = Order.objects.get_or_create(
            buyer=user_profile,
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
    user_profile = UserProfile.get_profile_by_user(user=request.user)
    orders = Order.objects.filter(buyer=user_profile)
    total_price = sum(order.total_price for order in orders)
    return render(request, 'carts/cart.html', {'orders': orders, 'total_price': total_price})

@login_required(login_url='login')
def edit_order(request, order_id):
    user_profile = UserProfile.get_profile_by_user(user=request.user)
    order = get_object_or_404(Order, id=order_id, buyer=user_profile)

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
    user_profile = UserProfile.get_profile_by_user(user=request.user)
    order = get_object_or_404(Order, id=order_id, buyer=user_profile)
    order.delete()
    messages.success(request, "Order removed successfully!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def process_payment(request):
    if request.method == 'GET':
        user_profile = UserProfile.get_profile_by_user(user=request.user)
        orders = Order.objects.filter(buyer=user_profile)
        
        total_price = sum(order.total_price for order in orders)

        if total_price > user_profile.balance:
            messages.error(request, "Insufficient balance to complete the payment.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        for order in orders:
            if order.quantity > order.product.quantity:
             messages.error(request, f"Insufficient stock for product: {order.product.name}.")
             return redirect(request.META.get('HTTP_REFERER', '/'))
            

        if total_price == 0:
            messages.error(request, "No orders in the cart to process payment.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        for order in orders:
            payment = Payment.objects.create(
                seller=order.seller,
                buyer=order.buyer,
                product=order.product,
                quantity=order.quantity,
                total_price=order.total_price,
                order_id=order.id
            )
            payment.process_payment()

        messages.success(request, "Payment processed successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
