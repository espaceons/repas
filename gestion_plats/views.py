from django.shortcuts import render
from django.views import View
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import logging

# Import de tous les modèles nécessaires
from menus.models import Menu
from plats.models import Plat
from recettes.models import Recette
from ingredients.models import Ingredient
from stock.models import Stock

logger = logging.getLogger(__name__)

class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        """Vue principale du tableau de bord avec toutes les statistiques"""
        context = {
            'section': 'dashboard',
            'error': None
        }

        try:
            # 1. Statistiques de base
            self._add_basic_stats(context)
            
            # 2. Données récentes
            self._add_recent_data(context)
            
            # 3. Gestion des stocks
            self._add_stock_data(context)
            
            # 4. Calcul des coûts moyens
            self._add_cost_data(context)

        except Exception as e:
            logger.error(f"Erreur dans DashboardView: {str(e)}", exc_info=True)
            context['error'] = "Certaines données sont temporairement indisponibles"

        return render(request, self.template_name, context)

    def _add_basic_stats(self, context):
        """Ajoute les statistiques de base au contexte"""
        context.update({
            'total_menus': Menu.objects.count(),
            'total_plats': Plat.objects.count(),
            'total_recettes': Recette.objects.count(),
            'total_ingredients': Ingredient.objects.count(),
        })

    def _add_recent_data(self, context):
        """Ajoute les données récentes au contexte"""
        try:
            context.update({
            'recent_menus': Menu.objects.select_related( 'user' ).order_by('-date_service')[:3],
            'recent_plats': Plat.objects.select_related('recette').prefetch_related('recette__compositions__ingredient')[:3]
        })            
        except Exception as e:
            logger.error(f"Error loading recent data: {e}")
        context.update({
            'recent_menus': [],
            'recent_plats': []
        })
        
        #context.update({
        #    'recent_menus': Menu.objects.select_related( 'user' ).order_by('-date_service')[:3],
        #    'recent_plats': Plat.objects.select_related('recette' ).prefetch_related('recette__ingredients')[:3],
        #})

    def _add_stock_data(self, context):
        """Gère les données de stock avec seuil d'alerte"""
        try:
            stock_alertes = Stock.objects.filter(
                quantite__lte=models.F('seuil_alerte')
            ).select_related('ingredient').order_by('quantite')
            
            # Calcul du déficit dans la vue
            for stock in stock_alertes:
                stock.deficit = max(stock.seuil_alerte - stock.quantite, 0)
            
            context.update({
                'stock_alertes': stock_alertes[:5],
                'stock_alert_count': stock_alertes.count(),
            })
        except ObjectDoesNotExist:
            context.update({
                'stock_alertes': [],
                'stock_alert_count': 0,
            })

    def _add_cost_data(self, context):
        """Calcule les coûts moyens"""
        try:
            # Coût moyen des recettes
            recettes = Recette.objects.annotate(
                cost=models.Sum(
                    models.F('compositionrecette__quantite') * 
                    models.F('compositionrecette__ingredient__prix_unitaire')
                )
            )
            avg_cost = recettes.aggregate(models.Avg('cost'))['cost__avg'] or 0
            
            context['cout_moyen_recette'] = round(avg_cost, 2)
            
        except Exception as e:
            logger.warning(f"Erreur calcul coût: {str(e)}")
            context['cout_moyen_recette'] = 0