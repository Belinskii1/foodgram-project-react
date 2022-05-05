from rest_framework import filters
from django_filters.rest_framework import (
    FilterSet, AllValuesMultipleFilter,
    ModelChoiceFilter, BooleanFilter
)

from .models import Recipe
from users.models import User


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    author = ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
