# backend/payments/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('pay/', views.payment_page, name='payment_page'),
]

# backend/backend/urls.py — добавь
path('', include('payments.urls')),