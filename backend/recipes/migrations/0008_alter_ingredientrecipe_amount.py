# Generated by Django 4.0.4 on 2022-05-05 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_favorite_shoppingcart_ingredientrecipe_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество ингридиентов 1')], verbose_name='Количество'),
        ),
    ]
