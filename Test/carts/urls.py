from django.urls import path
from . import views

urlpatterns = [
     path('cart', views.index, name='index'),
     path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
     path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('remove-order/<int:order_id>/', views.remove_order, name='remove_order'),
]