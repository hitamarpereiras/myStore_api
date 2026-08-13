from rest_framework import serializers
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'store',
            'customer',
            'name_customer',
            'phone',
            'observation',
            'address',
            'house_number',
            'latitude',
            'longitude',
            'total',
            'subtotal',
            'remaining',
            'payment_method',
            'rate_delivery',
            'code',
            'status',
            'itens',
            'created_at',
        ]

        read_only_fields = [
            'status',
            'created_at', 
            'updated_at'
        ]

class ConfirmDeliverySerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        required=True
    )