from django.contrib import admin
from apps.accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'telephone'
    )

    list_filter = (
        'is_active',
    )
    search_fields = (
        'email',
        'first_name',
        'telephone'
    )
