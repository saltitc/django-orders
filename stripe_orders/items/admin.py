from django.contrib import admin

from .models import CartItem, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
    fields = (
        "name",
        "description",
        "price",
        "stripe_product_price_id",
    )
    readonly_fields = ("stripe_product_price_id",)
    search_fields = ("name",)
    ordering = ("-name",)


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    list_display = ("item", "user")
    fields = ("item", "user")
