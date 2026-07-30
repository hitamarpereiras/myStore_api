from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.products.pagination import ProductsPagination

from services import (
    validators,
    pillow_svc,
    supabase_svc
)


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    parser_classes = [
        MultiPartParser,
        FormParser,

    ]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'category',
        'price',
        'name',
    ]

    def get_queryset(self):
        user = self.request.user
        store_id = self.request.query_params.get('store')

        print(f"User: {user}, Store ID: {store_id}")

        if user.is_superuser:
            return Product.objects.all().order_by('created_at')
        
        queryset = Product.objects.filter(
            owner=user
        ).order_by('-created_at')

        if store_id:
            queryset = queryset.filter(store=store_id).order_by('created_at')

        return queryset


    def create(self, request, *args, **kwargs):
        image = request.FILES.get('image')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if image:
            try:
                validators.validate_image(image)
                buffer, ext = pillow_svc.process_image(image, 1024, 1024)

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket='products'
                )

                image_url = upload["url"]
                image_path = upload["path"]

            except Exception as e:
                return Response(
                    {"message": f"Erro ao processar a imagem: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer.save(
            owner=request.user,
            image_url=image_url,
            image_path=image_path
        )

        return Response(
            {"message": "Produto criado com sucesso"},
            status=status.HTTP_201_CREATED
        )


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        image = request.FILES.get('image')

        image_url = None
        image_path = None

        if image:
            try:
                validators.validate_image(image)

                if instance.image_path:
                    supabase_svc.delete_image(
                        path=instance.image_path,
                        bucket='products'
                    )

                buffer, ext = pillow_svc.process_image(image, 1024, 1024)

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket='products'
                )

                image_url = upload["url"]
                image_path = upload["path"]

                serializer.save(
                    owner=request.user,
                    image_url=image_url,
                    image_path=image_path
                )

            except Exception as e:
                return Response(
                    {"message": f"Erro ao processar a imagem: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer.save(
            owner=request.user,
        )

        return Response(
            {"message": "Produto atualizado com sucesso"},
            status=status.HTTP_200_OK
        )


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.image_path:
            supabase_svc.delete_image(
                path=instance.image_path,
                bucket='products'
            )

        instance.delete()

        return Response(
            {"message": "Produto deletado com sucesso"},
            status=status.HTTP_204_NO_CONTENT
        )
