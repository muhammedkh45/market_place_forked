from django.urls import path
from . import views

urlpatterns = [
    path('', views.deposit_page, name='deposit_page'),  # GET - for the HTML form
    path('process-payment/', views.process_payment, name='process_payment'),  # POST - for API call
]
