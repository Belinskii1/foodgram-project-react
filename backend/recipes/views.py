from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend

from .filters import IngredientSearchFilter, AuthorAndTagFilter
from .models import (Favorite, Ingredient, IngredientRecipe,
                     Recipe, Tag, ShoppingCart)
from .pagination import RecipePagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, FavoriteSerializers)


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


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     # serializer_class = RecipeSerializer
#     pagination_class = RecipePagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = RecipeFilter
#     permission_classes = [IsOwnerOrReadOnly, ]

#     def get_serializer_class(self):
#         if self.action in ('list', 'retrieve'):
#             return RecipeSerializer
#         return RecipeWriteSerializer

#     @action(methods=['post', 'delete'], detail=True,
#             permission_classes=[IsAuthenticated])
#     def favorite(self, request, pk):
#         if request.method == 'POST':
#             data = {'user': request.user.id, 'recipe': pk}
#             serializer = FavoriteRecipeSerializer(
#                 data=data,
#                 context={'request': request}
#             )
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         elif request.method == 'DELETE':
#             user = request.user
#             recipe = get_object_or_404(Recipe, id=pk)
#             favorite = get_object_or_404(
#                 Favorite, user=user, recipe=recipe
#             )
#             favorite.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return None

#     @action(methods=['post', 'delete'], detail=True,
#             permission_classes=[IsAuthenticated])
#     def shopping_cart(self, request, pk):
#         if request.method == 'POST':
#             data = {'user': request.user.id, 'recipe': pk}
#             serializer = ShoppingCartSerializer(
#                 data=data,
#                 context={'request': request}
#             )
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         elif request.method == 'DELETE':
#             user = request.user
#             recipe = get_object_or_404(Recipe, id=pk)
#             favorite = get_object_or_404(
#                 ShoppingCart, user=user, recipe=recipe
#             )
#             favorite.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(detail=False, methods=['get'],
#             permission_classes=[IsAuthenticated])
    # def download_shopping_cart(self, request):
    #     ingredients = IngredientRecipe.objects.filter(
    #         recipe__shoppingcart__user=request.user).values(
    #         'ingredient__name', 'ingredient__measurement_unit', 'amount'
    #     )
    #     shopping_cart = '\n'.join([
    #         f'{ingredient["ingredient__name"]} - {ingredient["amount"]} '
    #         f'{ingredient["ingredient__measurement_unit"]}'
    #         for ingredient in ingredients
    #     ])
    #     filename = 'shopping_cart.txt'
    #     response = HttpResponse(shopping_cart, content_type='text/plain')
    #     response['Content-Disposition'] = f'attachment; filename={filename}'
    #     return response


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    filter_class = AuthorAndTagFilter
    permission_classes = [IsOwnerOrReadOnly]

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name="favorite",
        url_path="favorite",
        permission_classes=[IsAuthenticated],
        serializer_class=FavoriteSerializers
    )
    def favorite(self, request, pk=id):
        if request.method == 'POST':
            user = request.user
            recipe = self.get_object()
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({
                    'errors': 'Нельзя повторно добавить рецепт в избранное'
                }, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializers(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                Favorite, user=request.user, recipe__id=pk
            )
            favorite.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name="shopping_cart",
        url_path="shopping_cart",
        permission_classes=[IsAuthenticated],
        serializer_class=FavoriteSerializers
    )
    def shopping_cart(self, request, pk=id):
        if request.method == 'POST':
            user = request.user
            recipe = self.get_object()
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response({
                    'errors': 'Нельзя повторно добавить рецепт в корзину'
                }, status=status.HTTP_400_BAD_REQUEST)
            favorite = ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializers(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                ShoppingCart, user=request.user, recipe__id=pk
            )
            favorite.delete()
            return Response(
                f'Рецепт {favorite.recipe} удален из корзины у пользователя'
                f' {request.user}', status=status.HTTP_204_NO_CONTENT
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_name='download_shopping_cart',
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
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
