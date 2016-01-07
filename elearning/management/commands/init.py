from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group
from django.db import OperationalError
from elearning.models import UserELearning
from django.contrib.auth.models import User

def insert_data():
    # Store key: object returned
    groups = {
        "admin": None,
        "teacher": None,
        "student": None
    }

    for group in groups:
        groups[group] = Group.objects.create(name=group)

    UserELearning.objects.create_user("test_user", "test@gmail.com", "test_user", "first", "name", "hell")


class Command(BaseCommand):
    help = 'Initialises the database from scratch'

    def handle(self, *args, **options):
        self.stdout.write("Clearing tables")
        call_command("reset_db", verbosity=3, interactive=False)

        self.stdout.write("\nCreating tables")
        try:
            call_command("migrate", verbosity=3, interactive=False)
        except OperationalError:  # wtf mysql?
            self.stdout.write("\nRetrying Creating tables")
            call_command("migrate", verbosity=3, interactive=False)

        self.stdout.write("\nInserting data")
        insert_data()

        self.stdout.write("SUCCESS")
