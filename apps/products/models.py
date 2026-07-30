from django.db import models
from apps.categories.models import Category
from apps.stores.models import Store
from django.conf import settings


        
class Product(models.Model):
        owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            verbose_name='Proprietário',
            db_index=True
        )
        store = models.ForeignKey(
            Store,
            on_delete=models.CASCADE,
            verbose_name='Loja',
            related_name='products',
            db_index=True
        )
        name = models.CharField(
             max_length=100,
             verbose_name='Nome'
        )
        category = models.ManyToManyField(
                Category,
                verbose_name='Categorias',
                related_name='products'
        )
        description = models.TextField(
                default='Produto sem descrição',
                max_length=320,
                verbose_name='Descrição'
        )
        price = models.DecimalField(
                default=0,
                max_digits=10,
                decimal_places=2,
                verbose_name='Preço'
        )
        stock = models.IntegerField(
                default=0,
                verbose_name='Estoque'
        )
        image_url = models.URLField(
            blank=True,
            null=True,
            verbose_name='URL da Imagem'
        )
        image_path = models.URLField(
            blank=True,
            null=True,
            verbose_name='Caminho da Imagem'
        )
        created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Criado em',
        )
        updated_at = models.DateTimeField(
            auto_now=True,
            verbose_name='Atualizado em',
        )

        # a pedido do front-end

        crop_x = models.IntegerField(
            blank=True, 
            null=True,
            verbose_name='Eixo x'
        )
        crop_y = models.IntegerField(
            blank=True, 
            null=True,
            verbose_name='Eixo y'
        )
        crop_width = models.IntegerField(
            blank=True, 
            null=True,
            verbose_name='Corte Largura'
        )
        crop_height = models.IntegerField(
            blank=True, 
            null=True,
            verbose_name='Corte Altura'
        )

        class Meta:
            ordering = ['-updated_at']
            verbose_name = 'Produto'
            verbose_name_plural = 'Produtos'

        def __str__(self):
            return self.name

        def save(self, *args, **kwargs):
            if self.price:
                thisprice = str(self.price).replace(',', '.')

                self.price = thisprice

            return super().save(*args, **kwargs)