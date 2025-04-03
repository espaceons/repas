from django.db import models
from ingredients.models import Ingredient

class Stock(models.Model):
    ingredient = models.OneToOneField( Ingredient, on_delete=models.CASCADE, related_name='stock' )
    quantite = models.DecimalField( max_digits=10, decimal_places=2, verbose_name="Quantité en stock ")
    seuil_alerte = models.DecimalField( max_digits=10, decimal_places=2, default=0, verbose_name="Seuil d'alerte" )

    class Meta:
        verbose_name = "Stock"
        ordering = ['ingredient__nom']

    def __str__(self):
        return f"{self.ingredient.nom} - {self.quantite}{self.ingredient.unite_mesure}"

    def diminuer_stock(self, quantite_utilisee):
        """Diminue le stock et retourne True si opération réussie"""
        if self.quantite >= quantite_utilisee:
            self.quantite -= quantite_utilisee
            self.save()
            return True
        return False