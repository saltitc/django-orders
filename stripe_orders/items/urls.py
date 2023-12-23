from django.urls import path

from .views import CartView, ItemDetailView, ItemListView, add_to_cart

app_name = 'items'

urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('buy/<int:id>/', add_to_cart, name='add-to-cart'),
]
