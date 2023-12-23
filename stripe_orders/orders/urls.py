from django.urls import path

from .views import (CancelTemplateView, OrderCreateView, OrderDetailView,
                    OrderListView)

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='detail'),
    path('create_order/', OrderCreateView.as_view(), name='create'),
    path('canceled/', CancelTemplateView.as_view(), name='cancel'),
]
