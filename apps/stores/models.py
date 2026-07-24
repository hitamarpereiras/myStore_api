from django.db import models
from django.conf import settings

from services.idgenerator_svc import generate_idStore


class Store(models.Model):
    id = models.CharField(
        default=generate_idStore,
        primary_key=True,
        editable=False,
        max_length=6,
        verbose_name='ID'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='stores',
        verbose_name='Proprietário'
    )
    name = models.CharField(max_length=100, verbose_name='Nome')
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )
    address = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Endereço'
    )
    cnpj = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CNPJ'
    )
    avatar_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Avatar URL'
    )
    avatar_path = models.URLField(
        blank=True,
        null=True,
        verbose_name='Avatar Caminho'
    )
    instagram_url = models.URLField(
        blank=True, 
        null=True
    )
    facebook_url = models.URLField(
        blank=True, 
        null=True
    )
    other_url = models.URLField(
        blank=True, 
        null=True
    )
    color_palette = models.JSONField(
        blank=True,
        null=True,
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
        ordering = ['-created_at']
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'

    def __str__(self):
        return f"{self.name}"
