import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"Item: {self.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price["id"]
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product["id"],
            unit_amount=round(self.price * 100),
            currency="rub",
        )
        return stripe_product_price


class CartQuerySet(models.QuerySet):
    def get_total_cart_cost(self):
        return sum(cart_item.item.price for cart_item in self)

    def stripe_products(self):
        line_items = []
        for cart_item in self:
            item = {
                "price": cart_item.item.stripe_product_price_id,
                'quantity': 1,
            }
            line_items.append(item)
        return line_items


class CartItem(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f"{self.item.name} in the @{self.user.username} cart"

    def de_json(self):
        cart_item = {
            "item_name": self.item.name,
            "price": float(self.item.price),
        }
        return cart_item
