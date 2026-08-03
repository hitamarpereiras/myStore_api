from django.db import models
from django.conf import settings
from apps.stores.models import Store
from services.idgenerator_svc import generate_Code

class OrderStatus(models.TextChoices):
    PENDING = "pending", "pendente"
    DELIVERED = "delivered", "entregue"
    CANCELED = "canceled", "cancelado"


class Order(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        verbose_name='Loja',
        db_index=True,
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Cliente',
        db_index=True,
    )
    delivery_man = models.ForeignKey(
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name='Entregador'
    )
    name_customer = models.CharField(
        max_length=100,
        verbose_name='Nome do cliente'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Telefone'
    )
    observation = models.TextField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Observação'
    )
    address = models.TextField(
        max_length=200,
        verbose_name='Endereço'
    )
    house_number = models.CharField(
        blank=True,
        null=True,
        verbose_name='Número da casa'
    )
    latitude = models.DecimalField(
        blank=True, 
        null=True,
        max_digits=20, 
        decimal_places=6,
        verbose_name='Latitude'
    )
    longitude = models.DecimalField(
        blank=True, 
        null=True,
        max_digits=20, 
        decimal_places=6, 
        verbose_name='Longitude'
    )
    total = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        verbose_name='Total'
    )
    subtotal = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        verbose_name='Subtotal'
    )
    remaining = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        verbose_name='Troco'
    )
    payment_method = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Pago com'
    )
    rate_delivery = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        verbose_name='Taxa de Entrega'
    )
    code = models.CharField(
        max_length=5,
        default=generate_Code,
        verbose_name='Código Entrega'
    )
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Status"
    )
    itens = models.JSONField(
        verbose_name='Lista de Itens'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name_customer[:10]} - {self.phone[:5]}"