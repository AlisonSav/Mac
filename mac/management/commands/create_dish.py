from random import choice, randint

from django.core.management.base import BaseCommand

from faker import Faker
from faker_food import FoodProvider

from mac.models import Dish


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Indicates the number of Dish to be created",
        )

    def handle(self, *args, **options):
        for_who = ["F1", "F2", "FK"]
        fake = Faker("en_US")
        fake.add_provider(FoodProvider)
        Dish.objects.bulk_create(
            Dish(
                dish_title=fake.dish(),
                for_who=choice(for_who),
                restaurant_id=randint(5, 13),
            )
            for _ in range(options.get("count"))
        )
        self.stdout.write(
            self.style.SUCCESS(f"Added {options.get('count')} new Dishes")
        )
