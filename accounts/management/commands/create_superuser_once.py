import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.environ.get('SUPERUSER_NAME', 'admin'),
                email=os.environ.get('SUPERUSER_EMAIL', 'admin@placementcom'),
                password=os.environ.get('SUPERUSER_PASSWORD', 'admin123')
            )
            self.stdout.write('Superuser created!')
        else:
            self.stdout.write('Superuser already exists, skipping.')