from django.shortcuts import render


def profile(request):
    """ Display User's Profile. """

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
