from django.urls import path
from . import views

urlpatterns = [
    path('',views.account_page,name='Inventory'),
    path('item_detail_<int:id>/', views.item_detail, name='item_detail'),

    
]