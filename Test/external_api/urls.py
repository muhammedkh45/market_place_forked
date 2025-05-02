from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
app_name = 'external_api'
urlpatterns = [
    #path('', views.test_page, name='test_interface'),
    # Product endpoints
    path('products/', views.product_list, name='product-list'),
    
    # Order endpoints
    path('orders/', views.OrderCreateView.as_view(), name='order-create'),
    path('orders/create/', views.create_order, name='legacy-order-create'),
    
    # Transaction endpoints
    path('transactions/', views.transaction_list, name='transaction-list'),
    
    # Test interface
    path('test_interface/', views.test_page, name='test_interface'),
    
    # Authentication
    path('auth/', obtain_auth_token, name='api-token-auth'),
]