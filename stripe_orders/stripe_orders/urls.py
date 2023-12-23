from django.contrib import admin
from django.urls import include, path

from orders.views import stripe_webhook_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls', namespace='items')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('users/', include('users.urls', namespace='users')),
    path("webhook/stripe/", stripe_webhook_view, name="stripe_webhook"),
]

