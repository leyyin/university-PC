from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group
from django.db import OperationalError
from elearning.models import UserELearning, Subject, Course, Enrollment
from django.contrib.auth.models import User
from datetime import date

def insert_data():
    # Store key: object returned
    groups = {
        "admin": None,
        "teacher": None,
        "student": None
    }

    for group in groups:
        groups[group] = Group.objects.create(name=group)

    admin = UserELearning.objects.create_user(username="admin", email="admin@gmail.com", password="admin", first_name="first", last_name="name", address="hell")
    admin.add_to_group("admin")

    teacher = UserELearning.objects.create_user(username="teacher", email="teacher@gmail.com", password="teacher", first_name="first", last_name="name", address="hell")
    teacher.add_to_group("teacher")
    student = UserELearning.objects.create_user("student", "student@gmail.com", "student", "first", "name", "hell")
    student2 = UserELearning.objects.create_user("student2", "student2@gmail.com", "student2", "John", "Doe", "heaven")
    student.add_to_group("student")
    student2.add_to_group("student")

    computer_science_subject = Subject.objects.create(name="Computer Science")
    compilers = Course.objects.create(name="Compilers", subject=computer_science_subject, teacher= teacher)
    machine_learning = Course.objects.create(name="Machine Learning", subject=computer_science_subject, teacher= teacher)
    Enrollment.objects.create(user=student, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student2, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student, course=machine_learning, enroll_date=date(2015, 9, 3))


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
