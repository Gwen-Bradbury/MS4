from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_items

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_client_secret = settings.STRIPE_CLIENT_SECRET

    """ If There's Nothing in the Basket Display This """
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket")
        return redirect(reverse('gins'))

    """ Get Basket Total """
    current_basket = basket_items(request)
    total = current_basket['grand_total']
    """ Chenge Basket Total to Int """
    stripe_total = round(total * 100)
    """ Add Client Secret Key """
    stripe.api_key = stripe_client_secret
    """ Create Intent """
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'stripe_client_secret': intent.client_secret
    }

    return render(request, template, context)
