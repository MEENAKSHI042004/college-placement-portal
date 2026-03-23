import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@placement.com')
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email=email,
                password=os.environ.get('SUPERUSER_PASSWORD', 'admin123'),
                full_name=os.environ.get('SUPERUSER_NAME', 'Admin'),
            )
            self.stdout.write(f'Superuser created: {email}')
        else:
            self.stdout.write('Superuser already exists, skipping.')