from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        TagRecipeInline,
        IngredientRecipeInline,
    ]

class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportActionModelAdmin):
    resource_class = IngredientResource
    #list_display = [field.name for field in Ingredient._meta.fields if field.name != "id"]


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(TagRecipe)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
