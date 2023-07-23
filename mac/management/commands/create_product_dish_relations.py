from random import randint

from django.core.management.base import BaseCommand

from mac.models import Dish, Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of Restaurants to be created",
        )

    def handle(self, *args, **options):
        for _ in range(options.get("count")):
            try:
                dish = Dish.objects.get(id=randint(1, 1300))
                product = Product.objects.get(id=randint(1, 100))
                dish.product.add(product)
            except IndexError:
                print("Invalid dish")  # noqa T201
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Dish-Product relations"))
