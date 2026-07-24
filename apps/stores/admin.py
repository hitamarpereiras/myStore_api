from django.contrib import admin
from apps.stores.models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'phone', 
        'cnpj', 
        'created_at', 
        'updated_at'
    ]
    search_fields = [
        'name',
        'cnpj',
        'phone'
    ]
    readonly_fields = [
        'color_palette',
        'created_at',
        'updated_at'
    ]
