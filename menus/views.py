from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Prefetch

from plats.models import Plat
from recettes.models import CompositionRecette
from .models import Menu, MenuPlat
from django.forms import inlineformset_factory

# Liste des menus
class MenuListView(ListView):
    model = Menu
    template_name = 'menu/menu_list.html'
    context_object_name = 'menus'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('plats', queryset=Plat.objects.select_related('recette')),
            Prefetch('plats__recette__compositionrecette_set', 
                   queryset=CompositionRecette.objects.select_related('ingredient'))
        )

# Détail d'un menu
class MenuDetailView(DetailView):
    model = Menu
    template_name = 'menu/menu_detail.html'

# Création d'un menu
class MenuCreateView(CreateView):
    model = Menu
    template_name = 'menu/menu_form.html'
    fields = ['nom', 'date_service']
    success_url = reverse_lazy('menu-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['menuplats'] = MenuPlatFormSet(self.request.POST)
        else:
            context['menuplats'] = MenuPlatFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        menuplats = context['menuplats']
        self.object = form.save()
        if menuplats.is_valid():
            menuplats.instance = self.object
            menuplats.save()
        return super().form_valid(form)

MenuPlatFormSet = inlineformset_factory(
    Menu,
    MenuPlat,
    fields=('plat', 'ordre'),
    extra=1
)


# Modification d'un menu
class MenuUpdateView(UpdateView):
    model = Menu
    template_name = 'menu/menu_form.html'
    fields = ['nom', 'date_service']
    success_url = reverse_lazy('menu-list')

# Suppression d'un menu
class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'menu/menu_confirm_delete.html'
    success_url = reverse_lazy('menu-list')