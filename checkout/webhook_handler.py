from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from gins.models import Gin
from profiles.models import UserProfile

import json
import time


class StripeWebhookHandler:
    """ Stripe Webhooks """
    def __init__(self, request):
        self.request = request

    # Starts with _ To Indictate it Will Only Be Used In this View
    def _confirmation_email(self, order):
        """ Send Order Confirmation Email """
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        content = render_to_string(
            'checkout/confirmation_emails/confirmation_email_content.txt',
            {'order': order, 'contact_us_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            content,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """ Handle Unknown/Unexpected Webhooks """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
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
        """ Give Empty Strings in Shipping Info 'Null' Value """
        for field, value in shipping_info.address.items():
            if value == "":
                shipping_info.address[field] = None

        """ Update Profile Info When Save Info is Ticked """
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_info.phone
                profile.default_street_address1 = shipping_info.address.line1
                profile.default_street_address2 = shipping_info.address.line2
                profile.default_town_or_city = shipping_info.address.city
                profile.default_county = shipping_info.address.state
                profile.default_country = shipping_info.address.country
                profile.default_postcode = shipping_info.address.postal_code
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 7:
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
                time.sleep(5)

        if order_exists:
            """ Order Already Exists """
            self._confirmation_email(order)
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
                    user_profile=profile,
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
                """ Order Created by Webhook """
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} \
                        ERROR: {e}',
                    status=500
                    )
        self._confirmation_email(order)
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
