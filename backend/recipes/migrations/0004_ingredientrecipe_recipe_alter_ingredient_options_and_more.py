# Generated by Django 4.0.4 on 2022-04-30 11:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_ingredient_rename_tags_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Ингридиент в рецепте',
                'verbose_name_plural': 'Ингридиенты в рецептах',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='картинка')),
                ('name', models.CharField(max_length=70, unique=True, verbose_name='Название Рецепта')),
                ('text', models.TextField(verbose_name='описание')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Укажите время приготовления блюда')], verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингридиент', 'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='название Ингридиента'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('#0000FF', '#0000FF'), ('#FF7F50', '#FF7F50'), ('#FFD700', '#FFD700'), ('#008000', '#008000'), ('#00FF00', '#00FF00'), ('#808000', '#808000'), ('#FFA500', '#FFA500'), ('#FFC0CB', '#FFC0CB'), ('#FF0000', '#FF0000'), ('#FFFF00', '#FFFF00')], default='#0000FF', max_length=10, verbose_name='цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='название Тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='поле Slug'),
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag')),
            ],
            options={
                'verbose_name': 'Тег у рецепта',
                'verbose_name_plural': 'Теги у рецептов',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.ingredient', verbose_name='ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.TagRecipe', to='recipes.tag', verbose_name='теги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]