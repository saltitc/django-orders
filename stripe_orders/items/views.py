from django.http import JsonResponse
from django.views.generic import DetailView, ListView

from .models import CartItem, Item


class ItemDetailView(DetailView):
    template_name = "items/item_detail.html"
    model = Item
    context_object_name = "item"


class ItemListView(ListView):
    model = Item
    template_name = "items/item_list.html"
    context_object_name = "items"


class CartView(ListView):
    model = CartItem
    template_name = "items/cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


def add_to_cart(request, *args, **kwargs):
    item_id = kwargs['id']
    item = Item.objects.get(id=item_id)
    CartItem.objects.get_or_create(user=request.user, item=item)
    return JsonResponse({"status": "success"})
