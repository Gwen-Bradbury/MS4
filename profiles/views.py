from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Display User's Profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        """ Create New Instance of Profile Form Using Post Data """
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')

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
