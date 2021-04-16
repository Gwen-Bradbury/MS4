from django.contrib import admin
from .models import Gin, GinCategory


class GinAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'gincategory',
        'price',
        'image'
    )

    ordering = ('sku',)


class GinCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )


admin.site.register(Gin, GinAdmin)
admin.site.register(GinCategory, GinCategoryAdmin)
