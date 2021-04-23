from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket")
        return redirect(reverse('gins'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IjK1HI1JHr19NRbzbB0VkD9q9xA6BzzND0ybdUZyn6AGxKD7EljLz3Bgs6pZeSSFCmHPfJaMdJq7ejF7eZCF8hX006z0bbeFn',
        'client_secret': 'client_secret'
    }

    return render(request, template, context)
