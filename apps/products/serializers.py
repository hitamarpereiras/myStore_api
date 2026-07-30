from rest_framework import serializers
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'owner',
            'store',
            'name',
            'category',
            'description',
            'price',
            'stock',
            'image',
            'image_url',
            'image_path',
            'created_at',
            'updated_at',
            'crop_x',
            'crop_y',
            'crop_width',
            'crop_height',
        ]
        read_only_fields = [
            'id', 
            'owner',
            'image_url',
            'image_path',
            'created_at', 
            'updated_at'
        ]

    """Sobrescreve os métodos create e update para remover 
    o campo "image" antes de criar ou atualizar a instância"""

    def create(self, validated_data):
        validated_data.pop("image", None)
        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        validated_data.pop("image", None)
        return super().update(instance, validated_data)