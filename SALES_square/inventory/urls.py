from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.account_page,name='Inventory'),
    path('item_detail_<int:id>/', views.item_detail, name='item_detail'),
    path('<int:id>/edit', views.edit_item, name='edit_item'),
    path('add_item/',views.add_item, name='add_item'),
    path('add-category/', views.add_category, name='add_category'),
    path('remove-category/', views.remove_category, name='remove_category'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]