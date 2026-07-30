from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.stores.urls')),
    path('adm/', admin.site.urls),
]
