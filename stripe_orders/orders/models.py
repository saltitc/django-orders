import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from items.models import CartItem

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class Order(models.Model):
    CREATED = 0
    PAID = 1
    STATUSES = (
        (CREATED, "Created"),
        (PAID, "Paid"),
    )

    cart_history = models.JSONField(default=dict)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)

    def update_after_payment(self):
        cart_items = CartItem.objects.filter(user=self.customer)
        self.status = self.PAID
        self.cart_history = {
            "purchased_items": [cart_item.de_json() for cart_item in cart_items],
            "total_cost": float(cart_items.get_total_cart_cost()),
        }
        cart_items.delete()
        self.save()

    def __str__(self):
        return f"Order #{self.id}. {self.customer}"
