from django.urls import path
from stock.views import StockCreateView, StockDeleteView, StockListView, StockUpdateView, StockDetailView

app_name = 'stock'

urlpatterns = [
    path('', StockListView.as_view(), name='list'),
    path('create/', StockCreateView.as_view(), name='create'),
    path('update/<int:pk>/', StockUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', StockDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', StockDetailView.as_view(), name='detail'),
]