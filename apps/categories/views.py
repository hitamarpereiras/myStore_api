from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.none()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'owner', 'store']
    

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Category.objects.all().order_by('-updated_at')
        
        return Category.objects.filter(owner=user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)