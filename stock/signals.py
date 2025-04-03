from django.db.models.signals import post_save
from django.dispatch import receiver
from recettes.models import CompositionRecette
from stock.models import Stock

@receiver(post_save, sender=CompositionRecette)
def update_stock_on_recipe_use(sender, instance, created, **kwargs):
    if created:  # Seulement pour les nouvelles compositions
        try:
            stock = Stock.objects.get(ingredient=instance.ingredient)
            stock.diminuer_stock(instance.quantite)
        except Stock.DoesNotExist:
            pass  # Ou créer un stock avec quantité 0 si nécessaire