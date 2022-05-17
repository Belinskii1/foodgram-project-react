from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.filters import SearchFilter

from .models import Recipe


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


# class RecipeFilter(FilterSet):
#     tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
#     is_favorited = filters.BooleanFilter(method='filter_is_favorited')
#     is_in_shopping_cart = filters.BooleanFilter(
#         method='filter_is_in_shopping_cart'
#     )

#     class Meta:
#         model = Recipe
#         fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

#     def filter_is_favorited(self, queryset, name, value):
#         if value:
#             return queryset.filter(favorites__user=self.request.user)
#         return queryset

#     def filter_is_in_shopping_cart(self, queryset, name, value):
#         if value:
#             return queryset.filter(shopping_carts__user=self.request.user)
#         return queryset

class AuthorAndTagFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    is_favorited = CharFilter(method='filter_is_favorited')
    is_in_shopping_cart = CharFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(
            tags__slug__in=tags
        ).distinct()

    def filter_is_favorited(self, queryset, is_favorited, slug):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        is_favorited = self.request.query_params.get(
            'is_favorited',
        )
        if is_favorited:
            return queryset.filter(
                favorite__user=self.request.user
            ).distinct()
        return queryset

    def filter_is_in_shopping_cart(self, queryset, is_in_shopping_cart, slug):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart',
        )
        if is_in_shopping_cart:
            return queryset.filter(
                shoppingcart__user=self.request.user
            ).distinct()
        return queryset
