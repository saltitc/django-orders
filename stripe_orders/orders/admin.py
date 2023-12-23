from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        'id', 'created',
        'cart_history', 'status', 'customer'
    )
    readonly_fields = ('id', 'created')
