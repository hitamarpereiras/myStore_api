from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.orders.models import Order 
from apps.products.models import Product
import json


# Baixar o estoque altomaticamente

@receiver(pre_save, sender=Order)
def update_product_stock(sender, instance, **kwargs):

    # Se não esxistir no banco ignora
    if not instance.pk:
        return
    
    try:
        old_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return
    
    # só dispara quando status for de false para true
    if old_order.status == 'pendente' and instance.status == 'entregue':
        
        itens = instance.itens

        if not itens:
            return
        
        if isinstance(itens, str):
            itens = json.loads(itens)

        if isinstance(itens, dict):
            itens = [itens]

        for item in itens:
            product_id = item.get('id')
            quantity = item.get('quantity', 0)

            try:
                product = Product.objects.get(id=product_id)
                new_stock = product.stock - quantity

                # Não deixar estoque negativo
                product.stock = max(new_stock, 0)
                product.save()

            except Product.DoesNotExist:
                continue