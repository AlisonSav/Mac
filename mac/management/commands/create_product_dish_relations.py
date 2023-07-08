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
            dish = Dish.objects.get(id=randint(1, 100))
            product = Product.objects.get(id=randint(1, 100))
            dish.product.add(product)
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Dish-Product relations"))
