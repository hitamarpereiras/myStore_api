from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers import UserCreateSerializer, UserSerializer
from apps.accounts.models import User



class RegisterView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

class AccountViewSet(ModelViewSet):

    # Permissão de apenas esses metodos
    http_method_names = [
        "get",
        "patch",
        "head",
        "options",
    ]

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all().order_by('-id')

        return User.objects.filter(pk=user.pk).order_by('-id')
