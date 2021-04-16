from django.shortcuts import render, get_object_or_404
from .models import Gin


def all_gins(request):
    """ Shows All Gins, Including Searching and Sorting Queries """
    gins = Gin.objects.all()

    context = {
        'gins': gins,
    }

    return render(request, 'gins/gins.html', context)


def gin_detail(request, gin_id):
    """ Shows Individual Gin Details """
    gin = get_object_or_404(Gin, pk=gin_id)

    context = {
        'gin': gin,
    }

    return render(request, 'gins/gin_detail.html', context)
