from django.db import models


class Tags(models.Model):
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
