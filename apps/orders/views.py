from rest_framework import viewsets
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'code', 'total']

    def get_queryset(self):
        user = self.request.user

        qs = Order.objects.filter(store=user.store)

        if user.is_customer:
            return qs.filter(customer__user=user)

        if user.is_delivery:
            return qs.filter(delivery_man__user=user)

        if user.is_store:
            return qs

        return Order.objects.none()