from random import choice, randint

from django.core.management.base import BaseCommand

from faker import Faker

from mac.models import Restaurant


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            choices=range(1, 11),
            help="Indicates the number of Restaurants to be created",
        )

    def handle(self, *args, **options):
        size = ["S", "M", "L"]
        fake = Faker("en_US")
        available_list = []
        for i in range(30):
            i = randint(5, 230)
            if not Restaurant.objects.filter(area_id=i):
                available_list.append(i)
        Restaurant.objects.bulk_create(
            Restaurant(title=fake.company(), size=choice(size), area_id=choice(available_list))
            for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Restaurants"))
