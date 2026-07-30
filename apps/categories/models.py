from django.db import models
from django.conf import settings
from apps.stores.models import Store

class Category(models.Model):
        owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT,
            related_name='categories',
            verbose_name='Proprietário'
        )
        store = models.ForeignKey(
            Store,
            null=True,
            blank=True,
            on_delete=models.PROTECT,
            related_name='store',
            verbose_name='Loja'
        )
        name = models.CharField(
            unique=True,
            max_length=50,
            verbose_name='Categoria'
        )
        description = models.TextField(
            default='Categoria sem descrição',
            max_length=120,
            verbose_name='Descrição',
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
            ordering = ['-updated_at']
            verbose_name = 'Categoria'
            verbose_name_plural = 'Categorias'

        def __str__(self):
            return self.name

        def save(self, *args, **kwargs):
            if self.name:
                self.name = self.name.strip().lower()

            super().save(*args, **kwargs)