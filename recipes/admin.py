from django.contrib import admin
from .models import Recipe, RecipeCategory


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'recipecategory',
        'ingredients',
        'method',
        'garnish'
    )

    ordering = ('name',)


class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )


admin.site.register(Recipe)
admin.site.register(RecipeCategory)
