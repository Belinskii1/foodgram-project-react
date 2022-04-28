from django.db import models


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
        verbose_name = 'Название Тега'
    )
    color = models.CharField(
        choices=COLOR_CHOICES,
        default=BLUE,
        max_length=10,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Поле Slug'
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
        verbose_name = 'Название Ингридиента'
    )
    measurement_unit = models.CharField(
        choices=MEANSUREMENT_UNIT_CHOISES,
        max_length=10,
        verbose_name='единица измерения'
    )

    class Meta:
        verbose_name = 'Ннгридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name   
