from django.urls import path
from . import views

urlpatterns = [
    path('navbar-content/', views.navbar_view, name='your_view_that_renders_navbarwithoutforms'),
    path('', views.deposit_page, name='deposit_page'),  # GET - for the HTML form
    path('process-payment/', views.process_payment, name='process_payment'),  # POST - for API call
]
