from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404
    )
from django.contrib import messages
from django.db.models import Q
from .models import Gin


def all_gins(request):
    """ Shows All Gins, Including Searching and Sorting Queries """
    gins = Gin.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('gins'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            gins = gins.filter(queries)

    context = {
        'gins': gins,
        'search_input': query,
    }

    return render(request, 'gins/gins.html', context)


def gin_detail(request, gin_id):
    """ Shows Individual Gin Details """
    gin = get_object_or_404(Gin, pk=gin_id)

    context = {
        'gin': gin,
    }

    return render(request, 'gins/gin_detail.html', context)
