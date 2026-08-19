from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.db.models import QuerySet

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.products.pagination import ProductsPagination
from apps.stores.models import Store

from services import (
    validators,
    pillow_svc,
    supabase_svc
)


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        "category",
        "price",
        "name",
    ]

    def get_store(self):
        store_id = self.request.headers.get("X-Store-ID")

        if not store_id:
            raise PermissionDenied(
                "O header X-Store-ID é obrigatório."
            )

        try:
            return Store.objects.get(id=store_id)

        except Store.DoesNotExist:
            raise PermissionDenied(
                "Loja não encontrada."
            )

    def is_store_owner(self, store):
        user = self.request.user

        return (
            user.is_superuser
            or store.owner_id == user.id
        )

    def check_store_management_permission(self, store):
        """
        Verifica se o usuário pode criar, editar
        ou excluir produtos da loja.
        """

        if not self.is_store_owner(store):
            raise PermissionDenied(
                "Você não possui permissão para administrar "
                "os produtos desta loja."
            )

    def get_queryset(self) -> QuerySet:
        store = self.get_store()

        return (
            Product.objects
            .select_related("store")
            .filter(store=store)
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        store = self.get_store()

        # Customer pode visualizar produtos,
        # mas não pode criar.
        self.check_store_management_permission(store)

        image = request.FILES.get("image")

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        image_url = None
        image_path = None

        if image:
            try:
                validators.validate_image(image)

                buffer, ext = pillow_svc.process_image(
                    image,
                    1024,
                    1024
                )

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket="products"
                )

                image_url = upload["url"]
                image_path = upload["path"]

            except Exception as e:
                return Response(
                    {
                        "message": (
                            f"Erro ao processar a imagem: {str(e)}"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        product = serializer.save(
            owner=request.user,
            store=store,
            image_url=image_url,
            image_path=image_path
        )

        return Response(
            self.get_serializer(product).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # A loja do produto é a loja que será administrada.
        self.check_store_management_permission(
            instance.store
        )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        image = request.FILES.get("image")

        if image:
            try:
                validators.validate_image(image)

                if instance.image_path:
                    supabase_svc.delete_image(
                        path=instance.image_path,
                        bucket="products"
                    )

                buffer, ext = pillow_svc.process_image(
                    image,
                    1024,
                    1024
                )

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket="products"
                )

                product = serializer.save(
                    owner=request.user,
                    image_url=upload["url"],
                    image_path=upload["path"]
                )

            except Exception as e:
                return Response(
                    {
                        "message": (
                            f"Erro ao processar a imagem: {str(e)}"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            product = serializer.save(
                owner=request.user
            )

        return Response(
            self.get_serializer(product).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.check_store_management_permission(
            instance.store
        )

        if instance.image_path:
            supabase_svc.delete_image(
                path=instance.image_path,
                bucket="products"
            )

        instance.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )