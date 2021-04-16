from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404
    )
from django.contrib import messages
from django.db.models import Q
from .models import Gin, GinCategory


def all_gins(request):
    """ Shows All Gins, Including Searching and Sorting Queries """
    gins = Gin.objects.all()
    query = None
    gincategories = None

    if request.GET:
        if 'gincategory' in request.GET:
            gincategories = request.GET['gincategory'].split(',')
            gins = gins.filter(gincategory__name__in=gincategories)
            gincategories = GinCategory.objects.filter(name__in=gincategories)

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
        'current_gincategory': gincategories
    }

    return render(request, 'gins/gins.html', context)


def gin_detail(request, gin_id):
    """ Shows Individual Gin Details """
    gin = get_object_or_404(Gin, pk=gin_id)

    context = {
        'gin': gin,
    }

    return render(request, 'gins/gin_detail.html', context)
