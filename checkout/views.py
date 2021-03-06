from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from gins.models import Gin
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from basket.contexts import basket_items

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('stripe_client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_CLIENT_SECRET
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed. \
                            Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_client_secret = settings.STRIPE_CLIENT_SECRET
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        """ Put Form Data into Dictionary """
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
        }

        order_form = OrderForm(form_data)
        """ Save Valid Order Form """
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('stripe_client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            for item_id, item_count in basket.items():
                try:
                    gin = Gin.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        gin=gin,
                        quantity=item_count
                    )

                    order_line_item.save()

                except gin.DoesNotExist:
                    """ Item Not In DB """
                    messages.error(request, (
                        "One of the products in your basket wasn't found!"
                        "Please call us for assistance!")
                    )
                    """ Delete Empty Order and Return to Basket"""
                    order.delete()
                    return redirect(reverse('view_basket'))

            """ If User Saves Info to Profile """
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))
        else:
            """ If Form Not Valid """
            messages.error(request, 'There was an error with your form. \
                                Please double check your information.')
    else:
        """ If There's Nothing in the Basket Display This """
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "There's nothing in your basket")
            return redirect(reverse('gins'))

        """ Get Basket Total """
        current_basket = basket_items(request)
        total = current_basket['grand_total']
        """ Change Basket Total to Int """
        stripe_total = round(total * 100)
        """ Add Client Secret Key """
        stripe.api_key = stripe_client_secret
        """ Create Intent """
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'stripe_client_secret': intent.client_secret
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Successful Checkouts """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        """ Attach User's Profile to Order """
        order.user_profile = profile
        order.save()

        """ Save User's Info """
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_country': order.country,
                'default_postcode': order.postcode,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
