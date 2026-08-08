from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('', home),
    path('api/v1/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.categories.urls')),
    path('api/v1/', include('apps.stores.urls')),
    path('api/v1/', include('apps.products.urls')),
    path('api/v1/', include('apps.orders.urls')),
    path('api/v1/', include('apps.sales.urls')),
    path('adm/', admin.site.urls),
]
