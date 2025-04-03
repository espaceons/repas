from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecetteListView.as_view(), name='recette-list'),
    path('<int:pk>/', views.RecetteDetailView.as_view(), name='recette-detail'),
    path('create/', views.RecetteCreateView.as_view(), name='recette-create'),
    path('<int:pk>/update/', views.RecetteUpdateView.as_view(), name='recette-update'),
    path('<int:pk>/delete/', views.RecetteDeleteView.as_view(), name='recette-delete'),
]