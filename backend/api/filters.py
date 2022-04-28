from rest_framework import filters

class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'
