# Generated by Django 4.0.4 on 2022-04-28 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_tags_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Название Ингридиента')),
                ('measurement_unit', models.CharField(choices=[('кг', 'кг'), ('г', 'г'), ('л', 'л'), ('мл', 'мл'), ('шт', 'шт')], max_length=10, verbose_name='единица измерения')),
            ],
            options={
                'verbose_name': 'Ннгридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]