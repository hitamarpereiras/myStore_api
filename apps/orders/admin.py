from django.contrib import admin
from apps.orders.models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'name_customer',
        'phone',
        'total',
        'status',
        'created_at',
    ]
    search_fields = [
        'phone',
        'store',
        'created_at',
    ]