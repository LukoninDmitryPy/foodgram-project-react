import csv
from django.core.management import BaseCommand

from recipes_and_ingridients.models import Ingredient

TABLES_DICT = {
    Ingredient: 'ingridients.csv',
}


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        for model, base in TABLES_DICT.items():
            with open(
                f'{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully load data'))
