from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView, View

from .models import CartItem, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderDetailView(DetailView):
    template_name = "orders/order.html"
    model = Order
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Заказ #{self.object.id}"
        return context


class OrderListView(ListView):
    template_name = "orders/orders.html"
    queryset = Order.objects.all()
    ordering = "-created"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customer=self.request.user)


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.create(customer=self.request.user)
        cart_items = CartItem.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=cart_items.stripe_products(),
            metadata={"order_id": order.id},
            mode="payment",
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:detail', kwargs={'pk': order.id})}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:cancel')}",
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


class CancelTemplateView(TemplateView):
    template_name = "orders/canceled.html"
