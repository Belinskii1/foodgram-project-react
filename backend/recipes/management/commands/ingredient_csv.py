import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'ingredient from csv load'

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print('ингредиенты уже существуют')
            return

    def handle(self, *args, **options):
        with open('./ingredients.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1]
                        )
