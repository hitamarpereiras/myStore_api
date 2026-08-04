from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.accounts.serializers import UserCreateSerializer
from apps.accounts.models import User

class AccountViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all().order_by('-id')

        return User.objects.filter(pk=user.pk).order_by('-id')
