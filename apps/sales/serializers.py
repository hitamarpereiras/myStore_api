from rest_framework import serializers
from apps.sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            'id',
            'total',
            'subtotal',
            'remaining',
            'payment_method',
            'rate_delivery',
            'account',
            'order',
            'sotre',
            'collaborator',
            'observation',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields= [
            'account',
            'created_at', 
            'updated_at'
        ]