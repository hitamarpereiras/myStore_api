from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.orders.views import OrderViewSet, ConfirmDelivery


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('orders/<str:pk>/confirm-delivery', ConfirmDelivery.as_view(), name='confirm-delivery'),
    path('', include(router.urls)),
]