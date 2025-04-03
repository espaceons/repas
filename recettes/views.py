from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Recette, CompositionRecette
from django.forms import inlineformset_factory

# Liste des recettes
class RecetteListView(ListView):
    model = Recette
    template_name = 'recettes/recette_list.html'
    context_object_name = 'recettes'

# Détail d'une recette
class RecetteDetailView(DetailView):
    model = Recette
    template_name = 'recettes/recette_detail.html'

# Création d'une recette (avec gestion des ingrédients)
class RecetteCreateView(CreateView):
    model = Recette
    template_name = 'recettes/recette_form.html'
    fields = ['nom', 'description', 'temps_preparation', 'instructions']
    success_url = reverse_lazy('recette-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['compositions'] = CompositionFormSet(self.request.POST, instance=self.object)
        else:
            context['compositions'] = CompositionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        compositions = context['compositions']
        self.object = form.save()
        if compositions.is_valid():
            compositions.instance = self.object
            compositions.save()
        return super().form_valid(form)

# Modification d'une recette
class RecetteUpdateView(UpdateView):
    model = Recette
    template_name = 'recettes/recette_form.html'
    fields = ['nom', 'description', 'temps_preparation', 'instructions']
    success_url = reverse_lazy('recette-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['compositions'] = CompositionFormSet(self.request.POST, instance=self.object)
        else:
            context['compositions'] = CompositionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        compositions = context['compositions']
        self.object = form.save()
        if compositions.is_valid():
            compositions.instance = self.object
            compositions.save()
        return super().form_valid(form)

# Suppression d'une recette
class RecetteDeleteView(DeleteView):
    model = Recette
    template_name = 'recettes/recette_confirm_delete.html'
    success_url = reverse_lazy('recette-list')

# Formset pour les ingrédients
CompositionFormSet = inlineformset_factory(
    Recette, 
    CompositionRecette, 
    fields=('ingredient', 'quantite'), 
    extra=1, 
    can_delete=True
)