from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.customers.views import CustomerViewSet
from apps.customers.views import CustomerRgisterView


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('customers/register/', CustomerRgisterView.as_view(), name='register'),
    path('', include(router.urls)),
]