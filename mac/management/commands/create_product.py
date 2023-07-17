from random import randint

from django.core.management.base import BaseCommand

from faker import Faker
from faker_food import FoodProvider

from mac.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of products to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")
        fake.add_provider(FoodProvider)
        Product.objects.bulk_create(
            Product(product_title=fake.ingredient(), energy=randint(1, 100)) for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new products"))
