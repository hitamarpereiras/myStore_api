from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.sales.models import Sale
from apps.sales.serializers import SaleSerializer
from apps.stores.models import Store


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_store(self):
        """
        Obtém a loja enviada pelo frontend através do header:

            X-Store-ID: D8B509

        E verifica se essa loja pertence ao usuário autenticado.
        """

        store_id = self.request.headers.get("X-Store-ID")

        if not store_id:
            raise PermissionDenied(
                "O header X-Store-ID é obrigatório."
            )

        try:
            store = Store.objects.get(
                id=store_id,
                owner=self.request.user
            )
        except Store.DoesNotExist:
            raise PermissionDenied(
                "Você não tem acesso a esta loja."
            )

        return store

    def get_queryset(self):
        """
        Retorna somente as vendas da loja atualmente selecionada
        pelo usuário.
        """

        store = self.get_store()

        return Sale.objects.filter(
            account=self.request.user,
            store=store
        ).select_related(
            "order",
            "store",
            "account"
        )

    def perform_create(self, serializer):
        """
        Ao criar uma venda, a loja e a conta são determinadas
        pelo backend.

        O frontend não consegue criar uma venda em outra loja
        simplesmente alterando o JSON.
        """

        store = self.get_store()

        serializer.save(
            account=self.request.user,
            store=store
        )

        return Response(
            {"message": "Venda salva com sucesso!"},
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        """
        Impede que uma venda seja transferida para outra conta
        ou outra loja através do payload.
        """

        store = self.get_store()

        serializer.save(
            account=self.request.user,
            store=store
        )

        return Response(
            {"message": "Venda atualizada com sucesso!"},
            status=status.HTTP_200_OK
        )