from django.urls import path
from . import views
app_name = 'dashboard'


urlpatterns = [
    path('transaction-report/', views.transaction_report, name='transaction_report'),
    path('transaction/<int:id>/print/', views.print_transaction, name='print_transaction'),
    path('transaction/<int:id>/make-review/', views.make_review, name='make_review'),
]
