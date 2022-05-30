from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientRecipe,
                     Recipe, Tag, ShoppingCart)
from .pagination import RecipePagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, RecipeWriteSerializer,
                          FavoriteRecipeSerializer, TagSerializer,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_serializer_class(self):
        """разделяет типы запросов на списковые и одиночные"""
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """добавляет или удаляет рецепт в избранном"""
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = FavoriteRecipeSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                Favorite, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """добавляет или удаляет рецепт в корзине"""
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = ShoppingCartSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """скачивает список ингридиентов из рецептов в корзине"""
        ingredients = IngredientRecipe.objects.filter(
            recipe__shoppingcart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )
        shopping_cart = '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
