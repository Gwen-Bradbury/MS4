from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_recipes, name='view_recipes'),
    path('addrecipe/', views.add_recipe, name='add_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe')
]
