from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Load sample users."

    def handle(self, *args, **options):
        User.objects.create_superuser("admin@mail.com", "admin", type="G")
        User.objects.create_user("golden@mail.com", "golden", type="G")
        User.objects.create_user("silver@mail.com", "silver", type="S")
        User.objects.create_user("bronze@mail.com", "bronze", type="B")

        self.stdout.write(self.style.SUCCESS("Users loaded."))
