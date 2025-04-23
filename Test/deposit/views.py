from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentCardSerializer
from .models import Deposit
import uuid
from datetime import datetime
from django.shortcuts import render

# Helper functions (can go in utils.py)
def luhn_check(card_number: str) -> bool:
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def is_card_expired(month: str, year: str) -> bool:
    try:
        exp = datetime.strptime(f"{month}/{year}", "%m/%Y")
        return exp < datetime.now()
    except ValueError:
        return True

# API view to handle the POST request
@api_view(['POST'])
def process_payment(request):
    # Ensure request is in JSON format
    if not request.content_type == 'application/json':
        return Response({"error": "Content-type must be application/json"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = PaymentCardSerializer(data=request.data)
    
    # Check if the data is valid
    if serializer.is_valid():
        data = serializer.validated_data
        if not luhn_check(data['card_number']):
            return Response({"error": "Invalid card number."}, status=status.HTTP_400_BAD_REQUEST)
        if is_card_expired(data['expiration_month'], data['expiration_year']):
            return Response({"error": "Card expired."}, status=status.HTTP_400_BAD_REQUEST)

        deposit = Deposit.objects.create(
            amount=data['deposit_amount'],
            status='successful',
            transaction_id=str(uuid.uuid4())
        )

        # Return success response in JSON format
        return Response({
            "message": "Mock Deposit Successful",
            "transaction_id": deposit.transaction_id,
            "status": deposit.status,
            "amount": deposit.amount
        })
    
    # If serializer is invalid, return the error messages
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#HTML form view
def deposit_page(request):
    return render(request, 'deposit/deposit.html')