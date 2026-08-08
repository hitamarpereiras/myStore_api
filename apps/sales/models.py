from django.db import models
from apps.orders.models import Order
from apps.stores.models import Store
from django.conf import settings


class Sale(models.Model):
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
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Conta',
        related_name='accounts',
        db_index=True
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        verbose_name='Pedido',
        related_name='orders',
        db_index=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        verbose_name='Loja',
        related_name='stores',
        db_index=True
    )
    collaborator = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Colaborador'
    )
    observation = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Observação'
    )
    status = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em',
    )


    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_at}"