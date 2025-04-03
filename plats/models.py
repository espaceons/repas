from django.db import models
from django.core.validators import MinValueValidator
from ingredients.models import Ingredient
from recettes.models import Recette  # Importez le modèle Recette

class Plat(models.Model):
    TYPE_PLAT_CHOICES = [
        ('petit_dejeuner', 'Petit déjeuner'),
        ('dejeuner', 'Déjeuner'),
        ('diner', 'Dîner'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField()
    type_plat = models.CharField(max_length=20, choices=TYPE_PLAT_CHOICES)
    nombre_portions = models.PositiveIntegerField()
    date_preparation = models.DateField(auto_now_add=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE,
        null=True,  # Permet temporairement les valeurs NULL
        blank=True)  # Permet les champs vides dans les formulaires)


    def __str__(self):
        return f"{self.nom} ({self.get_type_plat_display()})"
    
    

class PlatIngredient(models.Model):
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE, verbose_name="Plat")
    ingredient = models.ForeignKey( Ingredient, on_delete=models.CASCADE, verbose_name="Ingrédient" )
    quantite = models.DecimalField(  max_digits=10, decimal_places=2, verbose_name="Quantité", validators=[MinValueValidator(0.01)] ) # Évite les quantités nulles

    class Meta:
        unique_together = ('plat', 'ingredient')  # Évite les doublons
        verbose_name = "Composition de plat"

    def __str__(self):
        return f"{self.quantite} {self.ingredient.unite_mesure} de {self.ingredient.nom} dans {self.plat.nom}"