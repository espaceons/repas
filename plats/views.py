from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Plat

# Liste des plats
class PlatListView(ListView):
    model = Plat
    template_name = 'plats/plat_list.html'
    context_object_name = 'plats'

# Détail d'un plat
class PlatDetailView(DetailView):
    model = Plat
    template_name = 'plats/plat_detail.html'

# Création d'un plat
class PlatCreateView(CreateView):
    model = Plat
    template_name = 'plats/plat_form.html'
    fields = ['nom', 'description', 'type_plat', 'nombre_portions']
    success_url = reverse_lazy('plat-list')

# Modification d'un plat
class PlatUpdateView(UpdateView):
    model = Plat
    template_name = 'plats/plat_form.html'
    fields = ['nom', 'description', 'type_plat', 'nombre_portions']
    success_url = reverse_lazy('plat-list')

# Suppression d'un plat
class PlatDeleteView(DeleteView):
    model = Plat
    template_name = 'plats/plat_confirm_delete.html'
    success_url = reverse_lazy('plat-list')