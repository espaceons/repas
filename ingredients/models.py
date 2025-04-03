from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Ingredient(models.Model):
    UNITE_MESURE_CHOICES = [
        ('kg', 'Kilogramme (kg)'),
        ('g', 'Gramme (g)'),
        ('l', 'Litre (l)'),
        ('ml', 'Millilitre (ml)'),
        ('m', 'Mètre (m)'),
        ('cm', 'Centimètre (cm)'),
        ('piece', 'Pièce'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    unite_mesure = models.CharField(max_length=50, choices=UNITE_MESURE_CHOICES, default='piece') # default value added
    quantite = models.DecimalField( max_digits=10, decimal_places=2, default=1.0, verbose_name="Quantité disponible" )
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire (TND)", validators=[MinValueValidator(0)])
    # Nouveaux champs temporels
    date_achat = models.DateField(null=True, blank=True, verbose_name="Date d'achat")  # Saisie manuelle
    date_validite = models.DateField( verbose_name="Date de validité", null=True, blank=True )

    def __str__(self):
        return f"{self.nom} ({self.quantite} {self.get_unite_mesure_display()})"