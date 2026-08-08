from django.contrib import admin
from apps.sales.models import Sale


@admin.register(Sale)
class AdminSales(admin.ModelAdmin):
    list_display = [
        'id',
        'total',
        'subtotal',
        'account',
        'order',
        'created_at'
    ]
    list_filter = ('created_at',)
    search_fields = ('account__name', 'order__id')
