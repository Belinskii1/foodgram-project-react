import os
import base64
from django.core import validators
from django.db import models
from django_base64field.fields import Base64Field

def image_as_base64(image_file, format='png'):
    if not os.path.isfile(image_file):
        return None
    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return 'data:image/%s;base64,%s' % (format, encoded_string)


class Tag(models.Model):
    BLUE = '#0000FF'
    CORAL = '#FF7F50'
    GOLD = '#FFD700'
    GREEN = '#008000'
    LIME = '#00FF00'
    OLIVE = '#808000'
    ORANGE = '#FFA500'
    PINK = '#FFC0CB'
    RED = '#FF0000'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, BLUE),
        (CORAL, CORAL),
        (GOLD, GOLD),
        (GREEN, GREEN),
        (LIME, LIME),
        (OLIVE, OLIVE),
        (ORANGE, ORANGE),
        (PINK, PINK),
        (RED, RED),
        (YELLOW, YELLOW),
    ]

    name = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        verbose_name = 'название Тега'
    )
    color = models.CharField(
        choices=COLOR_CHOICES,
        default=BLUE,
        max_length=10,
        verbose_name='цвет'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='поле Slug'
    )
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    KG = 'кг'
    G = 'г'
    L = 'л'
    ML = 'мл'
    UNIT = 'шт'

    MEANSUREMENT_UNIT_CHOISES = [
        (KG, KG),
        (G, G),
        (L, L),
        (ML, ML),
        (UNIT, UNIT),
    ]

    name = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        verbose_name = 'название Ингридиента'
    )
    measurement_unit = models.CharField(
        choices=MEANSUREMENT_UNIT_CHOISES,
        max_length=10,
        verbose_name='единица измерения'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name   


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name = 'ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name = 'теги'
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name = 'картинка'
        )
    name = models.CharField(
        max_length=70,
        unique=True,
        blank=False,
        null=False,
        verbose_name = 'Название Рецепта'
    )
    text = models.TextField(
        verbose_name = 'описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                0, message='Укажите время приготовления блюда'),
            ),
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name  


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'

    def __str__(self):
        return f'Рецепт {self.recipe.name} содержит ингридиент {self.ingredient.name}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тег у рецепта'
        verbose_name_plural = 'Теги у рецептов'

    def __str__(self):
        return f'У рецепта {self.recipe.name} есть тег {self.tag.name}'
