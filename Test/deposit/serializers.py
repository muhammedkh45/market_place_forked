from rest_framework import serializers

class PaymentCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    expiration_month = serializers.CharField(max_length=2)
    expiration_year = serializers.CharField(max_length=4)
    cvc = serializers.CharField(max_length=3)
    deposit_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
