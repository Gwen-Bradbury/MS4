from django.shortcuts import (
                              render,
                              redirect,
                              reverse,
                              get_object_or_404
                             )
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Gin, GinCategory
from .forms import GinForm


def all_gins(request):
    """ Shows All Gins, Including Searching and Sorting Queries """
    gins = Gin.objects.all()
    query = None
    gincategories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                gins = gins.annotate(lower_name=Lower('name'))
            if sortkey == 'gincategory':
                sortkey = 'gincategory__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            gins = gins.order_by(sortkey)

        if 'gincategory' in request.GET:
            """ Shows All Gin Categories """
            gincategories = request.GET['gincategory'].split(',')
            gins = gins.filter(gincategory__name__in=gincategories)
            gincategories = GinCategory.objects.filter(name__in=gincategories)

        if 'q' in request.GET:
            """ Search Bar Messages and Queries """
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('gins'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            gins = gins.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'gins': gins,
        'search_input': query,
        'current_gincategory': gincategories,
        'current_sorting': current_sorting,
    }

    return render(request, 'gins/gins.html', context)


def gin_detail(request, gin_id):
    """ Shows Individual Gin Details """
    gin = get_object_or_404(Gin, pk=gin_id)

    context = {
        'gin': gin,
    }

    return render(request, 'gins/gin_detail.html', context)


def add_gin(request):
    """ Add a product to the store """
    ginform = GinForm()
    template = 'gins/add_gin.html'
    context = {
        'ginform': ginform,
    }

    return render(request, template, context)
