from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from plats.models import Plat
from django.db.models import Sum

class Menu(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Créé par")
    nom = models.CharField(max_length=200, verbose_name="Nom du menu")
    date_service = models.DateField(verbose_name="Date de service")
    plats = models.ManyToManyField(Plat, through='MenuPlat', verbose_name="Plats composants")

    @property
    def calculer_cout_total(self):
        """Version sécurisée avec le bon nom de relation"""
        total = 0.0
        for plat in self.plats.all():
            if plat.recette:  # Vérifie si le plat a une recette
                for comp in plat.recette.compositionrecette_set.all():
                    if comp.ingredient:  # Vérifie si la composition a un ingrédient
                        total += float(comp.quantite) * float(comp.ingredient.prix_unitaire)
        return total
    
    @property
    def nombre_total_portions(self):
        """Retourne le nombre total de portions (version property)."""
        return self.plats.aggregate(total=Sum('nombre_portions'))['total'] or 0
    
    def __str__(self):
        return f"{self.nom} (Servi le {self.date_service.strftime('%d/%m/%Y')})"
    

    
class MenuPlat(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Menu")
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE, verbose_name="Plat")
    ordre = models.PositiveIntegerField( verbose_name="Ordre d'affichage", validators=[MinValueValidator(1)] )

    class Meta:
        ordering = ['ordre']  # Trie les plats par ordre
        unique_together = ('menu', 'plat')  # Un plat ne peut apparaître qu'une fois par menu

    def __str__(self):
        return f"{self.plat.nom} en position {self.ordre} dans {self.menu.nom}"