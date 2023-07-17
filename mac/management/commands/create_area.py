from django.core.management.base import BaseCommand

from faker import Faker
from mac.models import Area


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            # help="Indicates the number of Areas to be created",
        )

    def handle(self, *args, **options):
        fake = Faker("en_US")

        Area.objects.bulk_create(
            Area(area_title=fake.street_name(), country=fake.country()) for _ in range(options.get("count"))
        )
        self.stdout.write(self.style.SUCCESS(f"Added {options.get('count')} new Areas"))
