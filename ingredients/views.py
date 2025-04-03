# ingredients/views.py
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from stock.models import Stock
from .models import Ingredient
from .forms import IngredientForm

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient_list.html'
    context_object_name = 'ingredients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(nom__icontains=search_query)
        return queryset.order_by('nom')

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_form.html'
    success_url = reverse_lazy('ingredients:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'ingredients/ingredient_detail.html'
    context_object_name = 'ingredient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['used_in_recipes'] = self.object.compositionrecette_set.select_related('recette').all()
        return context

class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_form.html'
    success_url = reverse_lazy('ingredients:list')

class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'ingredients/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredients:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usage_count'] = self.object.compositionrecette_set.count()
        return context
    
    
class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        # Calcul des alertes stock
        stock_alertes = Stock.objects.filter(
            quantite__lte=models.F('seuil_alerte')
        ).select_related('ingredient')[:5]

        context = {
            # Vos données existantes...
            'total_menus': ...,
            'total_plats': ...,
            
            # Nouvelles données stock
            'stock_alertes': stock_alertes,
            'stock_alert_count': stock_alertes.count(),
        }
        return render(request, self.template_name, context)