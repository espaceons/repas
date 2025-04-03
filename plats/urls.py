from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlatListView.as_view(), name='plat-list'),
    path('<int:pk>/', views.PlatDetailView.as_view(), name='plat-detail'),
    path('create/', views.PlatCreateView.as_view(), name='plat-create'),
    path('<int:pk>/update/', views.PlatUpdateView.as_view(), name='plat-update'),
    path('<int:pk>/delete/', views.PlatDeleteView.as_view(), name='plat-delete'),
]