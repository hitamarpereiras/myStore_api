from rest_framework import serializers
from apps.stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Store
        fields = [
            'id',
            'owner',
            'name',
            'phone',
            'address',
            'cnpj',
            'avatar_url',
            'instagram_url',
            'facebook_url',
            'other_url',
            'color_palette',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['avatar_url', 'color_palette', 'created_at', 'updated_at']

        extra_kwargs = {
            'owner': {'read_only': True},
        }

    """Sobrescreve os métodos create e update para remover 
    o campo "image" antes de criar ou atualizar a instância"""

    def create(self, validated_data):
        validated_data.pop("image", None)
        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        validated_data.pop("image", None)
        return super().update(instance, validated_data)