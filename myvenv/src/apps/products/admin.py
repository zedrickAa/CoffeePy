from django.contrib import admin
from .models import Ingredient, ProductType, Product, Recipe
from django.utils.safestring import mark_safe


class RecipeInline(admin.TabularInline):
    """Tabular Inline View for Recipe"""

    model = Recipe
    extra = 0


class ProductAdmin(admin.ModelAdmin):

    readonly_fields = ("image_display",)
    inlines = [RecipeInline]

    def image_display(self, obj):
        return mark_safe(
            '<img src="{url}" style="max-width: 200px"/>'.format(url=obj.image.url)
        )


admin.site.register(Ingredient)
admin.site.register(ProductType)
admin.site.register(Product, ProductAdmin)