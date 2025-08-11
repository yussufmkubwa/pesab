from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

class Command(BaseCommand):
    help = 'Creates five dummy users for testing purposes.'

    def handle(self, *args, **options):
        User = get_user_model()
        fake = Faker()

        for _ in range(5):
            username = fake.user_name()
            password = 'dummypassword'
            email = fake.email()

            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password, role='farmer')
                self.stdout.write(self.style.SUCCESS(f'Successfully created dummy user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Dummy user "{username}" already exists.'))
