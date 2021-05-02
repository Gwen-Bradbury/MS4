from django.shortcuts import (
                              render
                             )
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
        'current_sorting': current_sorting,
    }

    return render(request, 'recipes/recipes.html', context)


def add_recipe(request):
    """ Add a product to the store """
    recipeform = RecipeForm()
    template = 'recipes/add_recipe.html'
    context = {
        'recipeform': recipeform,
    }

    return render(request, template, context)
