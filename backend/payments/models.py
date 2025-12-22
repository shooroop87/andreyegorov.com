# backend/payments/models.py
from django.db import models

class PaymentConfig(models.Model):
    """Единственная запись с настройками платежа"""
    title = models.CharField('Название услуги', max_length=255, default='Оплата услуг')
    description = models.TextField('Описание', blank=True)
    amount = models.DecimalField('Сумма (руб)', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Настройка платежа'
        verbose_name_plural = 'Настройки платежа'
    
    def __str__(self):
        return f"{self.title} — {self.amount} ₽"
    
    def amount_in_kopecks(self):
        return int(self.amount * 100)