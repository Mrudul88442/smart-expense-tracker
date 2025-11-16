from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheme_name', 'scheme_code', 'units', 'purchase_price', 'purchase_date')
