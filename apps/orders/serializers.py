from rest_framework import serializers
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
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
            'created_at', 
            'updated_at'
        ]