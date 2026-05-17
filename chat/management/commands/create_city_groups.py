from django.core.management.base import BaseCommand
from chat.models import ChatGroup

CITY_GROUPS = [
    {"name": "Paris - Students", "city": "Paris"},
    {"name": "Lyon - Students", "city": "Lyon"},
    {"name": "Marseille - Students", "city": "Marseille"},
]


class Command(BaseCommand):
    help = "Create default city chat groups"

    def handle(self, *args, **options):
        created = 0
        for data in CITY_GROUPS:
            _, was_created = ChatGroup.objects.get_or_create(
                city=data["city"],
                defaults={"name": data["name"]},
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {data['name']}"))
            else:
                self.stdout.write(f"Already exists: {data['name']}")
        self.stdout.write(self.style.SUCCESS(f"Done — {created} group(s) created."))
