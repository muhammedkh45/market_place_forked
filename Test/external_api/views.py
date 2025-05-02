from django.shortcuts import render
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dashboard.models import Transaction
from carts.models import Order, Payment
from items.models import Category, Items
from core.models import UserProfile
from django.contrib.auth.models import User
from .serializers import ProductSerializer, CreateOrderSerializer
from .authentication import APIKeyAuthentication
from .models import APIClient

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def product_list(request):
#     """List all available products with stock"""
#     products = Items.objects.filter(
#         for_sale=True, 
#         Available_Stock=True
#     ).select_related('owned_by__user')
    
#     serializer = ProductSerializer(products, many=True)
#     return Response({
#         'status': 'success',
#         'count': products.count(),
#         'products': serializer.data
#     })

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @transaction.atomic
# def create_order(request):
#     """Legacy order creation endpoint (consider deprecating)"""
#     serializer = OrderCreateSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         product = Items.objects.select_for_update().get(
#             id=serializer.validated_data['product_id'],
#             for_sale=True,
#             Available_Stock=True
#         )
#         buyer_profile = request.user.profile
#         quantity = serializer.validated_data['quantity']

#         if product.quantity < quantity:
#             return Response(
#                 {'error': f'Only {product.quantity} items available'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Process through Payment model
#         payment = Payment.objects.create(
#             buyer=buyer_profile,
#             seller=product.owned_by,
#             product=product,
#             quantity=quantity,
#             total_price=product.price * quantity
#         )

#         if not payment.process_payment():
#             raise Exception("Payment processing failed")

#         return Response({
#             'success': True,
#             'order_id': payment.order_id,
#             'new_balance': buyer_profile.balance
#         }, status=status.HTTP_201_CREATED)

#     except Items.DoesNotExist:
#         return Response(
#             {'error': 'Product not available'}, 
#             status=status.HTTP_404_NOT_FOUND
#         )
#     except Exception as e:
#         return Response(
#             {'error': str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def transaction_list(request):
#     """Get authenticated user's transaction history"""
#     transactions = Transaction.objects.filter(
#         buyer__user=request.user
#     ).select_related('buyer', 'seller', 'product').order_by('-date')
    
#     serializer = TransactionSerializer(transactions, many=True)
#     return Response({
#         'status': 'success',
#         'count': transactions.count(),
#         'transactions': serializer.data
#     })

# def test_page(request):
#     """Render API test interface"""
#     return render(request, 'api/test_api.html')

# class OrderCreateView(APIView):
#     """Modern order creation endpoint using class-based view"""
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def post(self, request):
#         try:
#             data = request.data
#             product = Items.objects.select_for_update().get(
#                 id=data['product_id'],
#                 for_sale=True,
#                 Available_Stock=True
#             )
#             buyer_profile = request.user.profile
#             quantity = int(data.get('quantity', 1))

#             # Validate inventory
#             if product.quantity < quantity:
#                 return Response(
#                     {'error': f'Only {product.quantity} available'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Process payment
#             payment = Payment.objects.create(
#                 buyer=buyer_profile,
#                 seller=product.owned_by,
#                 product=product,
#                 quantity=quantity,
#                 total_price=product.price * quantity
#             )
            
#             if not payment.process_payment():
#                 return Response(
#                     {'error': 'Payment processing failed'},
#                     status=status.HTTP_402_PAYMENT_REQUIRED
#                 )

#             return Response({
#                 'status': 'success',
#                 'order_id': payment.order_id,
#                 'new_balance': buyer_profile.balance
#             }, status=status.HTTP_201_CREATED)

#         except KeyError:
#             return Response(
#                 {'error': 'Missing product_id or quantity'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Items.DoesNotExist:
#             return Response(
#                 {'error': 'Product not available'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        

#     def test_page(request):
#         categories = Category.objects.all()
#         items = Items.objects.filter(
#         Available_Stock=True,
#         is_approved=True,  # If you have approval system
#         quantity__gt=0,
#         ).select_related('owned_by__user').order_by('-date_added')
#         context = {'categories': categories, 'items': items} 
#         return render(request, 'api/test_api.html', context)

# class UserProductList(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user_products = Items.objects.filter(user=request.user)
#         serializer = ProductSerializer(user_products, many=True)
#         return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([APIKeyAuthentication])
def product_list(request):
    products = Items.objects.filter(advertise=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([APIKeyAuthentication])
def create_order(request):
    api_client_id = request.data.get('items', [])[0].get('api_client')
    client = APIClient.objects.filter(id=api_client_id).first()
    
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()

        # Create a dictionary of remaining quantities_advertise
        product_ids = [item['item_id'] for item in request.data.get('items', [])]
        quantities = {
            product.id: product.quantity_advertise
            for product in Items.objects.filter(id__in=product_ids, advertise=True)
        }
       

        return Response({
            "message": "Order created successfully", "order_id": order.id,
            "total_price": order.total_price,
            "remaining_quantities": quantities,
            "balance": client.user_profile.balance,

            }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)