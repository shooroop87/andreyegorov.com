# backend/payments/admin.py
from django.contrib import admin
from .models import PaymentConfig

@admin.register(PaymentConfig)
class PaymentConfigAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'is_active']
    list_editable = ['amount', 'is_active']