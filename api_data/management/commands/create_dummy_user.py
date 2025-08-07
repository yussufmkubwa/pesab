from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a dummy user for testing purposes.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'dummyuser'
        password = 'dummypassword'
        email = 'dummy@example.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, email=email, password=password, role='default')
            self.stdout.write(self.style.SUCCESS(f'Successfully created dummy user: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Dummy user "{username}" already exists.'))
