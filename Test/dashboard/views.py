from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from .models import Transaction
from core.models import Review
from django import forms

def transaction_report(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Not allowed")
    
    user_profile = request.user.profile

    if request.user.is_staff:
        transactions = Transaction.objects.all().order_by('-date')
    else:
        transactions = Transaction.objects.filter(buyer=user_profile).order_by('-date')

    return render(request, 'dashboard/transaction_report.html', {'transactions': transactions})

def print_transaction(request, id):
    transaction = get_object_or_404(Transaction, transaction_id=id)
    return render(request, 'dashboard/print_transaction.html', {'transaction': transaction})

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
