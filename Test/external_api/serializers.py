from rest_framework import serializers
from dashboard.models import Transaction
from items.models import Items
from carts.models import Order
from core.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'balance']
        read_only_fields = fields

class ProductSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(source='owned_by')
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Items
        fields = [
            'id', 'name', 'price', 'description',
            'quantity', 'seller', 'category',
            'average_rating', 'image'
        ]
        read_only_fields = ['seller']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Items.objects.filter(id=value, for_sale=True).exists():
            raise serializers.ValidationError("Product not available for sale")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    buyer = UserProfileSerializer()
    seller = UserProfileSerializer()
    product = ProductSerializer()

    class Meta:
        model = Transaction
        fields = [
            'transaction_id', 'buyer', 'seller',
            'product', 'quantity', 'total_price',
            'status', 'date'
        ]
        read_only_fields = fields