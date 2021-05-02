from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


def profile(request):
    """ Display User's Profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        """ Create New Instance of Profile Form Using Post Data """
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        """ Populate Form with Users Current Profile Info """
        form = UserProfileForm(instance=profile)
    """ Get Users Previous Orders """
    orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def previous_orders(request, order_number):
    """ View Users Previous Orders in checkout_success.html """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This confirmation for order number {order_number} \
             is a previous order. '
        'A confirmation email was sent when the order was origionally placed.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
