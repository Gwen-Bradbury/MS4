from django.shortcuts import render
from .models import Gin


def all_gins(request):
    """ Shows All Gins, Including Searching and Sorting Queries """
    gins = Gin.objects.all()

    context = {
        'gins': gins,
    }

    return render(request, 'gins/gins.html', context)
