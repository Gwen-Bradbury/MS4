from django.shortcuts import (
                              render,
                              redirect,
                              reverse,
                              get_object_or_404
                             )
from django.contrib import messages
from django.db.models.functions import Lower

from .models import Recipe, RecipeCategory
from .forms import RecipeForm


def view_recipes(request):
    """ Shows All Recipes, Including Sorting Queries """
    recipes = Recipe.objects.all()
    recipecategories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                recipes = recipes.annotate(lower_name=Lower('name'))
            if sortkey == 'recipecategory':
                sortkey = 'recipecategory__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            recipes = recipes.order_by(sortkey)

        if 'recipecategory' in request.GET:
            """ Shows All Recipe Categories """
            recipecategories = request.GET['recipecategory'].split(',')
            recipes = recipes.filter(recipecategory__name__in=recipecategories)
            recipecategories = RecipeCategory.objects.filter(
                name__in=recipecategories)

    current_sorting = f'{sort}_{direction}'

    context = {
        'recipes': recipes,
        'current_recipecategory': recipecategories,
        'current_sorting': current_sorting
    }

    return render(request, 'recipes/recipes.html', context)


def add_recipe(request):
    """ Add Recipe """
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe_form.save()
            messages.success(request, 'Recipe successfully added')
            return redirect(reverse('add_recipe'))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        recipe_form = RecipeForm()

    template = 'recipes/add_recipe.html'
    context = {
        'recipe_form': recipe_form
    }

    return render(request, template, context)


def edit_recipe(request, recipe_id):
    """ Edit Recipe """
    """ Prefill Form """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            recipe_form.save()
            messages.success(request, 'Recipe successfully updated')
            return redirect(reverse('view_recipes'))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        recipe_form = RecipeForm(instance=recipe)
        messages.info(request, f'You are editing {recipe.name}')

    template = 'recipes/edit_recipe.html'
    context = {
        'recipe_form': recipe_form,
        'recipe': recipe
    }

    return render(request, template, context)
