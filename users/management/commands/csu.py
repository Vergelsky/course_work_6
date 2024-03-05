from django.core.management import BaseCommand
import os
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('SUPERUSER_EMAIL'),
            first_name=os.getenv('SUPERUSER_FIRST_NAME'),
            last_name=os.getenv('SUPERUSER_LAST_NAME'),
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
