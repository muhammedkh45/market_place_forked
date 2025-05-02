from rest_framework import serializers
from dashboard.models import Transaction
from items.models import Items
from carts.models import Order
from core.models import UserProfile
# from .models import Order, OrderItem
from carts.models import Payment
from .models import APIClient


# class UserProfileSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     email = serializers.CharField(source='user.email')

#     class Meta:
#         model = UserProfile
#         fields = ['id', 'username', 'email', 'balance']
#         read_only_fields = fields

# class ProductSerializer(serializers.ModelSerializer):
#     seller = UserProfileSerializer(source='owned_by')
#     average_rating = serializers.SerializerMethodField()

#     class Meta:
#         model = Items
#         fields = [
#             'id', 'name', 'price', 'description',
#             'quantity', 'seller', 'category',
#             'average_rating', 'image'
#         ]
#         read_only_fields = ['seller']

#     def get_average_rating(self, obj):
#         return obj.get_average_rating()

# class OrderCreateSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField(min_value=1)
#     quantity = serializers.IntegerField(min_value=1)

#     def validate_product_id(self, value):
#         if not Items.objects.filter(id=value, for_sale=True).exists():
#             raise serializers.ValidationError("Product not available for sale")
#         return value

# class TransactionSerializer(serializers.ModelSerializer):
#     buyer = UserProfileSerializer()
#     seller = UserProfileSerializer()
#     product = ProductSerializer()

#     class Meta:
#         model = Transaction
#         fields = [
#             'transaction_id', 'buyer', 'seller',
#             'product', 'quantity', 'total_price',
#             'status', 'date'
#         ]
#         read_only_fields = fields

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'name', 'price', 'description', 
        'quantity_advertise', 'average_rating' ]

class OrderItemInputSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    api_client = serializers.IntegerField()

    def validate_item_id(self, value):
        """Validate that item exists"""
        if not Items.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Item ID {value} does not exist.")
        return value

class CreateOrderSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    total_price=0

    def validate(self, data):
        for entry in data['items']:
            try:
            # Fetch the item based on item_id
                item = Items.objects.get(id=entry['item_id'])
                api_client = APIClient.objects.get(id=entry['api_client'])
            except Items.DoesNotExist:
                raise serializers.ValidationError(f"Item ID {entry['item_id']} not found.")
            except APIClient.DoesNotExist:
                raise serializers.ValidationError(f"API client ID {entry['api_client']} not found.")
            
            # Check stock availability
            if entry['quantity'] > item.quantity_advertise:
                raise serializers.ValidationError(
                f"Not enough stock for {item.name}. Available: {item.quantity_advertise}, requested: {entry['quantity']}"
                )
            
            
        return data

    def create(self, validated_data):
        total_price = 0  # Initialize total_price to 0
        # order = Order.objects.create()
        # for entry in validated_data['items']:
        #     item = Items.objects.get(id=entry['item_id'])
        #     quantity = entry['quantity']
        #     OrderItem.objects.create(order=order, item=item, quantity=quantity)
        #     item.quantity -= quantity
        #     item.save()
        # return order
        
        for entry in validated_data['items']:
            item = Items.objects.get(id=entry['item_id'])
            quantity = entry['quantity']
            api_client = APIClient.objects.get(id=entry['api_client'])
            # Initialize total_price if not already initialized
            if 'total_price' not in locals():
                total_price = 0

            # Check if the buyer has enough balance
            total_price += item.price * entry['quantity']
            if api_client.user_profile.balance < total_price:
                raise serializers.ValidationError(
                    f"Insufficient balance."
                )

            order = Order.objects.create(buyer=api_client.user_profile,
                seller=item.owned_by,
                product=item,
                quantity=quantity)
            payment = Payment.objects.create(
                buyer=api_client.user_profile,
                seller=item.owned_by,
                product=item,
                quantity=quantity,
                total_price=item.price * quantity,
                order_id=order.id
            )
            payment.process_payment()
            item.quantity_advertise -= quantity
            item.save()
        return payment

