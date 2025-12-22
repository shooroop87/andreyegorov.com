# backend/payments/views.py
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import PaymentConfig

def payment_page(request):
    config = PaymentConfig.objects.filter(is_active=True).first()
    
    context = {
        'config': config,
        'terminal_key': settings.TBANK_TERMINAL_KEY,
    }
    return render(request, 'payments/pay.html', context)