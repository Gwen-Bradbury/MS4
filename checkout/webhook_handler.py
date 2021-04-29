from django.http import HttpResponse

from .models import Order, OrderLineItem
from gins.models import Gin

import json
import time


class StripeWebhookHandler:
    """ Stripe Webhooks """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle Unknown/Unexpected Webhooks """
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200
            )

    def handle_payment_succeeded(self, event):
        """ Handle payment_intent.succeeded Webhook """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        shipping_info = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)
        # Give Empty Strings in Shipping Info 'Null' Value
        for field, value in shipping_info.address.items():
            if value == "":
                shipping_info.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_info.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_info.phone,
                    street_address1__iexact=shipping_info.address.line1,
                    street_address2__iexact=shipping_info.address.line2,
                    town_or_city__iexact=shipping_info.address.city,
                    county__iexact=shipping_info.address.state,
                    country__iexact=shipping_info.address.country,
                    postcode__iexact=shipping_info.address.postal_code,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} \
                    | SUCCESS: Order already in database',
                status=200
                )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_info.name,
                    email=billing_details.email,
                    phone_number=shipping_info.phone,
                    street_address1=shipping_info.address.line1,
                    street_address2=shipping_info.address.line2,
                    town_or_city=shipping_info.address.city,
                    county=shipping_info.address.state,
                    country=shipping_info.address.country,
                    postcode=shipping_info.address.postal_code,
                    original_basket=basket,
                    stripe_pid=pid
                )

                for item_id, item_count in json.loads(basket).items():
                    gin = Gin.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        gin=gin,
                        quantity=item_count
                    )

                    order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} \
                        ERROR: {e}',
                    status=500
                    )
        return HttpResponse(
            content=f'Webhook received: {event["type"]} \
                 | SUCCESS: Created order with webhook',
            status=200
            )

    def handle_payment_failed(self, event):
        """ Handle payment_intent.payment_failed Webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
            )
