from django.shortcuts import (
                              render,
                              redirect,
                              reverse,
                              get_object_or_404
                             )
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        'gin': gin
    }

    return render(request, 'gins/gin_detail.html', context)


@login_required
def add_gin(request):
    """ Superuser Access Only """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, owners only function')
        return redirect(reverse('home'))
    """ Add Gin """
    if request.method == 'POST':
        gin_form = GinForm(request.POST, request.FILES)
        if gin_form.is_valid():
            gin = gin_form.save()
            messages.success(request, 'Gin successfully added')
            return redirect(reverse('gin_detail', args=[gin.id]))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        gin_form = GinForm()

    template = 'gins/add_gin.html'
    context = {
        'gin_form': gin_form,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def edit_gin(request, gin_id):
    """ Superuser Access Only """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, owners only function')
        return redirect(reverse('home'))
    """ Edit Gin """
    """ Prefill Form """
    gin = get_object_or_404(Gin, pk=gin_id)
    if request.method == 'POST':
        gin_form = GinForm(request.POST, request.FILES, instance=gin)
        if gin_form.is_valid():
            gin_form.save()
            messages.success(request, 'Gin successfully updated')
            return redirect(reverse('gin_detail', args=[gin.id]))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        gin_form = GinForm(instance=gin)
        messages.info(request, f'You are editing {gin.name}')

    template = 'gins/edit_gin.html'
    context = {
        'gin_form': gin_form,
        'gin': gin,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def delete_gin(request, gin_id):
    """ Superuser Access Only """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, owners only function')
        return redirect(reverse('home'))
    """ Delete Gin """
    gin = get_object_or_404(Gin, pk=gin_id)
    gin.delete()
    messages.success(request, 'Gin deleted')
    return redirect(reverse('gins'))
