from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from deposit.models import Deposit
from core.models import Review
from django import forms
from itertools import chain  # Import chain
from django.contrib import messages
from django.urls import reverse
from core.models import UserProfile

def transaction_report(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    user_profile = UserProfile.get_profile_by_user(request.user)
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
    transaction1 = get_object_or_404(Transaction, transaction_id=id)
    print(transaction1)
    product = transaction1.product
    user_profile = UserProfile.get_profile_by_user(request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            if not Review.objects.filter(user=user_profile, product=product,transaction=transaction1).exists():
                review = form.save(commit=False)
                review.transaction = transaction1
                review.product = product
                review.user = user_profile
                review.save()
                product.average_rating = Review.get_average_rating(product)
                product.save()
                messages.success(request, "Review submitted successfully!")
                return redirect(reverse('dashboard:transaction_report'))
            else:
                messages.error(request, "You have already submitted a review for this product.")
                return redirect(reverse('dashboard:transaction_report'))

        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = ReviewForm()
    return render(request, 'dashboard/make_review.html', {'form': form, 'product': product})
