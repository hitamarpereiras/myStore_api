from rest_framework.serializers import ModelSerializer
from apps.categories.models import Category

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'owner',
            'store', # é obrigatorio manadar o ID da loja
            'name',
            'description',
        ]

        read_only_fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
        ]