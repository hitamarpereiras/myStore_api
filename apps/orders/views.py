from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.views import APIView
from apps.orders.models import Order
from rest_framework import status
from rest_framework.response import Response
from apps.orders.serializers import OrderSerializer, ConfirmDeliverySerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from apps.stores.models import Store


class ConfirmDelivery(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        serializer = ConfirmDeliverySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(Order, pk=pk)

        # Verifica se o pedido pertence ao entregador
        """if order.delivery_man.user != request.user:
            return Response(
                {
                    "detail": (
                        "Você não pode confirmar este pedido."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )"""

        # Só permite confirmar pedidos pendentes
        if order.status != "pendente":
            return Response(
                {
                    "detail": (
                        "Este pedido não está pendente."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        code = serializer.validated_data["code"]

        if order.code != code:
            return Response(
                {
                    "detail": "Código inválido."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = "entregue"
        order.save()

        return Response(
            {
                "detail": "Entrega confirmada com sucesso."
            },
            status=status.HTTP_200_OK
        )


class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_at", "code", "total"]

    def get_store(self):

        store_id = self.request.headers.get("X-Store-ID")

        if not store_id:
            raise PermissionDenied(
                "O header X-Store-ID é obrigatório."
            )

        try:
            return Store.objects.get(
                id=store_id
            )
        except Store.DoesNotExist:
            raise PermissionDenied(
                "Loja não encontrada."
            )

    def get_queryset(self):
        user = self.request.user
        store = self.get_store()

        # Cliente:
        # retorna somente os pedidos dele
        # dentro da loja selecionada
        if hasattr(user, "customer"):
            return Order.objects.filter(
                store=store,
                customer=user
            )

        # Usuário da loja:
        # retorna todos os pedidos daquela loja
        return Order.objects.filter(
            store=store
        )

    def perform_create(self, serializer):
        user = self.request.user
        store = self.get_store()

        serializer.save(
            store=store,
            customer=user
        )