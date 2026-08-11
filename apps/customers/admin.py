from django.contrib import admin
from apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'address',
        'coins',
        'premium',
        'created_at'
    ]
    list_filter = ['created_at', 'updated_at', 'premium']
    search_fields = ['name', 'phone', 'address', 'premium']
