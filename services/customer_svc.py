from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.customers.models import Customer
from apps.accounts.models import User

from services import (
    validators,
    pillow_svc,
    supabase_svc
)


class CustomerService:

    @staticmethod
    @transaction.atomic
    def register_customer(validated_data):
        
        #Cria User + Customer, processa imagem e atualiza os campos adicionais
        
        image = validated_data.pop("image", None)
        email = validated_data.pop("email").strip().lower()
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name").strip().title()
        last_name = validated_data.pop("last_name").strip().title()
        telephone = validated_data.pop("telephone", None)

        if telephone:
            telephone = telephone.strip()

        # Verifica o Email
        if User.objects.filter(email=email).exists():
            raise ValidationError("Esse email já esta cadastrado!")

        # Criar User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            telephone=telephone
        )

        # Criar Customer
        customer = Customer.objects.create(
            user=user,
            **validated_data
        )

        avatar_url = None
        avatar_path = None

        if image:
            try:
                validators.validate_image(image)
                buffer, ext = pillow_svc.process_image(image, 300, 300)

                upload = supabase_svc.upload_image(
                    file_bytes=buffer.getvalue(),
                    ext=ext,
                    bucket='clientes'
                )

                avatar_url = upload["url"]
                avatar_path = upload["path"]

            except Exception as e:
                raise ValidationError(f"Erro ao processar a imagem")

        # Atualizar a account
        customer.avatar_url = avatar_url
        customer.avatar_path = avatar_path
        customer.save()

        return customer