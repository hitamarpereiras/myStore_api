from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from apps.stores.models import Store
from apps.stores.serializers import StoreSerializer

from services import (
    validators,
    pillow_svc,
    supabase_svc,
    colors_svc
)

class StoreViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Store.objects.all().order_by('-created_at')
    serializer_class = StoreSerializer
    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'owner',
        'cnpj',
    ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Store.objects.all().order_by('-created_at')

        return Store.objects.filter(owner=self.request.user).order_by('-created_at')


    def create(self, request, *args, **kwargs):
        image = request.FILES.get('image')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if image:
            try:
                validators.validate_image(image)
                buffer, ext = pillow_svc.process_image(image, 300, 300)

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket='avatar_lojas'
                )

                pallette_colors = colors_svc.get_this_colors(buffer)
                avatar_url = upload["url"]
                avatar_path = upload["path"]

            except Exception as e:
                return Response(
                    {"message": f"Erro ao processar a imagem: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer.save(
            owner=request.user,
            avatar_url=avatar_url,
            avatar_path=avatar_path,
            color_palette=pallette_colors
        )

        return Response(
            {"message": "Loja criada com sucesso"},
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

        avatar_url = None
        avatar_path = None
        pallette_colors = None

        if image:
            try:
                validators.validate_image(image)

                if instance.avatar_path:
                    supabase_svc.delete_image(
                        path=instance.avatar_path,
                        bucket='avatar_lojas'
                    )

                buffer, ext = pillow_svc.process_image(image, 300, 300)

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket='avatar_lojas'
                )

                pallette_colors = colors_svc.get_this_colors(buffer)
                avatar_url = upload["url"]
                avatar_path = upload["path"]

                serializer.save(
                    owner=request.user,
                    avatar_url=avatar_url,
                    avatar_path=avatar_path,
                    color_palette=pallette_colors
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
            {"message": "Loja atualizada com sucesso"},
            status=status.HTTP_200_OK
        )


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.avatar_path:
            supabase_svc.delete_image(
                path=instance.avatar_path,
                bucket='avatar_lojas'
            )

        instance.delete()

        return Response(
            {"message": "Loja deletada com sucesso"},
            status=status.HTTP_204_NO_CONTENT
        )
