from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from .models import Transaction
from deposit.models import Deposit
from core.models import Review
from django import forms
from itertools import chain  # Import chain

def transaction_report(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    user_profile = request.user.profile

    if request.user.is_staff:
        transactions = Transaction.objects.all().order_by('-date')
        deposits = Deposit.objects.all().order_by('-date')
    else:
        transactions = Transaction.objects.filter(
            buyer=user_profile
        ).union(
            Transaction.objects.filter(seller=user_profile)
        ).order_by('-date')
        deposits = Deposit.objects.filter(user=user_profile).order_by('-date') # Corrected to user

    # Add a 'type' field to distinguish between models
    transactions_with_type = [
        {'type': 'Transaction', 'data': t} for t in transactions
    ]
    deposits_with_type = [
        {'type': 'Deposit', 'data': d} for d in deposits
    ]

    # Combine and sort
    combined_data = sorted(
        chain(transactions_with_type, deposits_with_type),
        key=lambda item: item['data'].date,  # Sort by the 'date' attribute of the original model
        reverse=True,  # Order by descending date (most recent first)
    )

    return render(request, 'dashboard/transaction_report.html', {
        'combined_data': combined_data,
        'user_profile': user_profile,
    })


def print_transaction(request, id):
    transaction = get_object_or_404(Transaction, transaction_id=id)
    return render(request, 'dashboard/print_transaction.html', {'transaction': transaction})

def print_deposit(request, id):
    deposit = get_object_or_404(Deposit, id=id)
    return render(request, 'dashboard/print_deposit.html', {'deposit': deposit})    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

def make_review(request, id):
    transaction = get_object_or_404(Transaction, transaction_id=id)
    product = transaction.product
    user_profile = request.user.profile

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = product
            review.user = user_profile
            review.save()
            return HttpResponse("Review submitted successfully!")
    else:
        form = ReviewForm()

    return render(request, 'dashboard/make_review.html', {'form': form, 'product': product})
