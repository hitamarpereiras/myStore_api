from django.contrib import admin
from apps.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'owner',
        'store',
        'name',
        'created_at'
    ]
    list_filter = [
        'owner',
        'updated_at'
    ]
    search_fields = [
        'name',
        'owner',
        'store'
    ]