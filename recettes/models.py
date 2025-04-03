from django.db import models
from ingredients.models import Ingredient

class Recette(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    temps_preparation = models.PositiveIntegerField(help_text="Temps en minutes")
    instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='CompositionRecette')

    def __str__(self):
        return self.nom

    def cout_total(self):
        """Calcule le coût total de la recette"""
        return sum(
            comp.quantite * comp.ingredient.prix_unitaire
            for comp in self.compositionrecette_set.all()  # Notez le nom corrigé
        )

    @classmethod
    def get_average_cost(cls):
        """Calcule le coût moyen des recettes"""
        total = sum(recette.cout_total() for recette in cls.objects.all())
        count = cls.objects.count()
        return total / count if count > 0 else 0

class CompositionRecette(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantite = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('recette', 'ingredient')