from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer, RegisterCustomerSerializer

from services.customer_svc import CustomerService
from services import (
    validators,
    pillow_svc,
    supabase_svc
)

class CustomerRgisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # serve para chamar o serviço de criação de cliente
        CustomerService.register_customer(serializer.validated_data)

        return Response(
            {"message": "Usuário criado com sucesso"},
            status=status.HTTP_201_CREATED
        )
 

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    parser_classes = [MultiPartParser, FormParser]


    def get_queryset(self):
        user = self.request.user
        
        if user.is_authenticated:
            return Customer.objects.filter(user=user)
        
        return Customer.objects.none()


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

        save_data = {
            "user": request.user
        }

        if image:
            try:
                validators.validate_image(image)

                if instance.avatar_path:
                    supabase_svc.delete_image(
                        path=instance.avatar_path,
                        bucket='clientes'
                    )

                buffer, ext = pillow_svc.process_image(image, 300, 300)

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket='clientes'
                )

                avatar_url = upload["url"]
                avatar_path = upload["path"]


                save_data.update({
                    "avatar_url": avatar_url,
                    "avatar_path": avatar_path,
                })

            except Exception as e:
                return Response(
                    {"message": f"Erro ao processar a imagem: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer.save(**save_data)

        return Response(
            {"message": "Usuário atualizado com sucesso"},
            status=status.HTTP_200_OK
        )


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.avatar_path:
            supabase_svc.delete_image(
                path=instance.avatar_path,
                bucket='clientes'
            )

        instance.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )