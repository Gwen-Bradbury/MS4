from django.db import models


class RecipeCategory(models.Model):

    class Meta:
        verbose_name_plural = 'Recipe Categories'

    name = models.CharField(max_length=150)
    friendly_name = models.CharField(max_length=150, default="", blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Recipe(models.Model):
    image_url = models.URLField(max_length=1024, default="", blank=True)
    image = models.ImageField(default="", blank=True)
    recipecategory = models.ForeignKey(
        'RecipeCategory', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    ingredients = models.TextField()
    method = models.TextField()
    garnish = models.TextField()

    def __str__(self):
        return self.name
