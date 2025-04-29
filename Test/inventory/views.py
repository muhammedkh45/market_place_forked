from django.shortcuts import render, redirect

from .models import Account  

def account_page(request):
    account = None  # default

    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            account = None

    return render(request, 'inventory.html', {'account': account})
