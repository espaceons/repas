from django.urls import path
from . import views

urlpatterns = [
    path('', views.MenuListView.as_view(), name='menu-list'),
    path('<int:pk>/', views.MenuDetailView.as_view(), name='menu-detail'),
    path('create/', views.MenuCreateView.as_view(), name='menu-create'),
    path('<int:pk>/update/', views.MenuUpdateView.as_view(), name='menu-update'),
    path('<int:pk>/delete/', views.MenuDeleteView.as_view(), name='menu-delete'),
]