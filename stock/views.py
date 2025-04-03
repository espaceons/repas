from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from ingredients.models import Ingredient
from stock.forms import StockUpdateForm
from stock.models import Stock

class StockListView(ListView):
    model = Stock
    template_name = 'stock/stock_list.html'
    context_object_name = 'stock_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        return context
    
    
class StockCreateView(CreateView):
    model = Stock
    success_url = '/stock/'  # URL de redirection
    fields = ['ingredient', 'quantite', 'seuil_alerte']
    
    def get_success_url(self):
        messages.success(self.request, "Stock ajouté avec succès !")
        return reverse('stock:list')
    
    def form_valid(self, form):
        """Vérifie si un stock existe déjà pour cet ingrédient"""
        ingredient = form.cleaned_data['ingredient']
        if Stock.objects.filter(ingredient=ingredient).exists():
            messages.error(self.request, "Erreur : Stock déjà existant")
            return redirect('stock:list')
        response = super().form_valid(form)
        messages.success(self.request, f"Stock pour {self.object.ingredient.nom} créé !")
        return response
    
class StockUpdateView(UpdateView):
    model = Stock
    fields = ['quantite', 'seuil_alerte']
    template_name = 'stock/stock_form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Stock mis à jour avec succès !")
        return reverse('stock:list')

class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'stock/stock_confirm_delete.html'
    
    def get_success_url(self):
        messages.success(self.request, "Stock supprimé avec succès !")
        return reverse('stock:list')
    
class StockDetailView(UpdateView):  # Hérite de UpdateView pour combiner affichage et édition
    model = Stock
    form_class = StockUpdateForm
    template_name = 'stock/stock_detail.html'
    context_object_name = 'stock'
    
    
    def get_context_data(self, **kwargs):
        """Ajoute le calcul du déficit au contexte"""
        context = super().get_context_data(**kwargs)
        
        # Récupère l'objet Stock courant
        stock = self.object
        
        # Calcul sécurisé du pourcentage
        try:
            if stock.seuil_alerte > 0:
                percentage = (stock.quantite / stock.seuil_alerte) * 100
                context['pourcentage_stock'] = min(round(percentage, 2), 100)  # Limité à 100%
            else:
                context['pourcentage_stock'] = 100
        except (TypeError, AttributeError):
            context['pourcentage_stock'] = 0
        
        # Calcule le déficit (seuil_alerte - quantite, minimum 0)
        context['deficit'] = max(stock.seuil_alerte - stock.quantite, 0)
        
        # Ajoute d'autres données si nécessaire
        context['pourcentage_stock'] = (stock.quantite / stock.seuil_alerte * 100) if stock.seuil_alerte > 0 else 0
        
        return context

    def get_success_url(self):
        messages.success(self.request, "Stock mis à jour avec succès !")
        return reverse('stock:detail', kwargs={'pk': self.object.pk})
    
