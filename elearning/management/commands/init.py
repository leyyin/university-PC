from datetime import date

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import OperationalError


from elearning.models import UserELearning, Subject, Course, Enrollment, AssignmentGroup, Assignment, StudentAssignment
from elearning.utils import create_forums_course


def insert_data():
    # Store  key: object returned
    groups = {
        "admin": None,
        "teacher": None,
        "assistant": None,
        "student": None
    }

    # add groups
    for group in groups:
        groups[group] = Group.objects.create(name=group)

    # add users
    admin = UserELearning.objects.create_user(username="admin", email="admin@gmail.com", password="admin",
                                              first_name="Jesus", last_name="Wagner", address="hell")
    admin.grant_admin_rights()

    teacher = UserELearning.objects.create_user(username="teacher", email="teacher@gmail.com", password="teacher",
                                                first_name="Derrick", last_name="Grant", address="hell")
    teacher.add_to_group("teacher")

    teacher2 = UserELearning.objects.create_user(username="teacher2", email="teacher2@gmail.com", password="teacher2",
                                                first_name="Ernest", last_name="Haynes", address="hell")
    teacher2.add_to_group("teacher")

    teacher3 = UserELearning.objects.create_user(username="teacher3", email="teacher3@gmail.com", password="teacher3",
                                                first_name="Franklin", last_name="Moore", address="hell")
    teacher3.add_to_group("teacher")

    teacher4 = UserELearning.objects.create_user(username="teacher4", email="teacher4@gmail.com", password="teacher4",
                                                first_name="Ginger", last_name="Peterson", address="hell")
    teacher4.add_to_group("teacher")

    teacher5 = UserELearning.objects.create_user(username="teacher5", email="teacher5@gmail.com", password="teacher5",
                                                first_name="Dolores", last_name="Joseph", address="hell")
    teacher5.add_to_group("teacher")

    assistant = UserELearning.objects.create_user(username="assistant", email="assistant@gmail.com", password="assistant",
                                                first_name="Judy", last_name="Riley", address="hell")
    assistant.add_to_group("assistant")
    assistant2 = UserELearning.objects.create_user(username="assistant2", email="assistant2@gmail.com", password="assistant2",
                                                first_name="Owen", last_name="Parks", address="hell")
    assistant2.add_to_group("assistant")
    assistant3 = UserELearning.objects.create_user(username="assistant3", email="assistant3@gmail.com", password="assistant3",
                                                first_name="Bruce", last_name="Carpenter", address="hell")
    assistant3.add_to_group("assistant")
    student = UserELearning.objects.create_user("student", "student@gmail.com", "student", "Beatrice", "Stevenson", "hell")
    student2 = UserELearning.objects.create_user("student2", "student2@gmail.com", "student2", "John", "Doe", "heaven")
    student3 = UserELearning.objects.create_user("student3", "student3@gmail.com", "student3", "Carl", "Nelson", "heaven")
    student4 = UserELearning.objects.create_user("student4", "student4@gmail.com", "student4", "Edwin", "Simmons", "heaven")
    student5 = UserELearning.objects.create_user("student5", "student5@gmail.com", "student5", "Allen", "Williams", "heaven")
    student6 = UserELearning.objects.create_user("student6", "student6@gmail.com", "student6", "Alfred", "Castillo", "heaven")
    student7 = UserELearning.objects.create_user("student7", "student7@gmail.com", "student7", "Pat", "Thomas", "heaven")
    student8 = UserELearning.objects.create_user("student8", "student8@gmail.com", "student8", "Billy", "Barnes", "heaven")
    student9 = UserELearning.objects.create_user("student9", "student9@gmail.com", "student9", "Darnell", "Manning", "heaven")
    student10 = UserELearning.objects.create_user("student10", "student10@gmail.com", "student10", "Sherri", "Gomez", "heaven")
    student11 = UserELearning.objects.create_user("student11", "student11@gmail.com", "student11", "Celia", "Johnston", "heaven")
    student12 = UserELearning.objects.create_user("student12", "student12@gmail.com", "student12", "Terence", "Price", "heaven")
    student13 = UserELearning.objects.create_user("student13", "student13@gmail.com", "student13", "Angelica", "Cooper", "heaven")
    student14 = UserELearning.objects.create_user("student14", "student14@gmail.com", "student14", "Randolph", "Rios", "heaven")
    student15 = UserELearning.objects.create_user("student15", "student15@gmail.com", "student15", "Inez", "Burke", "heaven")
    student16 = UserELearning.objects.create_user("student16", "student16@gmail.com", "student16", "Garrett", "Stone", "heaven")
    student17 = UserELearning.objects.create_user("student17", "student17@gmail.com", "student17", "Leo", "Adams", "heaven")
    student18 = UserELearning.objects.create_user("student18", "student18@gmail.com", "student18", "Alejandro", "Ward", "heaven")
    student.add_to_group("student")
    student2.add_to_group("student")
    student3.add_to_group("student")
    student4.add_to_group("student")
    student5.add_to_group("student")
    student6.add_to_group("student")
    student7.add_to_group("student")
    student8.add_to_group("student")
    student9.add_to_group("student")
    student10.add_to_group("student")
    student11.add_to_group("student")
    student12.add_to_group("student")
    student13.add_to_group("student")
    student14.add_to_group("student")
    student15.add_to_group("student")
    student16.add_to_group("student")
    student17.add_to_group("student")
    student18.add_to_group("student")

    # add subjects and courses
    math_subject = Subject.objects.create(name="Math")
    computer_science_subject = Subject.objects.create(name="Computer Science")
    biology_subject = Subject.objects.create(name="Biology")
    physics_subject = Subject.objects.create(name="Physics")
    chemistry_subject = Subject.objects.create(name="Chemistry")
    microeconomics_subject = Subject.objects.create(name="Microeconomics")
    macroeconomics_subject = Subject.objects.create(name="Macroeconomics")
    history_subject = Subject.objects.create(name="History")
    music_subject = Subject.objects.create(name="Music")
    arithmetic = Course.objects.create(name="Arithmetic", subject=math_subject, teacher=teacher2)
    prealgebra = Course.objects.create(name="Pre-algebra", subject=math_subject, teacher=teacher2)
    basic_geometry = Course.objects.create(name="Basic-geometry", subject=math_subject, teacher=teacher2)

    compilers = Course.objects.create(name="Compilers", subject=computer_science_subject, teacher=teacher)
    machine_learning = Course.objects.create(name="Machine Learning", subject=computer_science_subject, teacher=teacher)
    web_programming = Course.objects.create(name="Web Programming", subject=computer_science_subject, teacher=teacher3)

    human_biology = Course.objects.create(name="Human biology", subject=biology_subject, teacher= teacher4)
    evolution = Course.objects.create(name="Evolution and the three of life", subject = biology_subject, teacher= teacher4)

    geometric_optics = Course.objects.create(name="Geometric optics", subject=physics_subject, teacher=teacher2)

    redox_reactions = Course.objects.create(name="Redox reactions", subject=chemistry_subject, teacher= teacher2)

    Enrollment.objects.create(user=student, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student, course=web_programming, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student2, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student2, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student2, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student3, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student3, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student3, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student4, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student4, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student4, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student5, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student5, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student5, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student6, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student6, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student6, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student7, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student7, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student7, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student8, course=compilers, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student8, course=machine_learning, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student8, course=web_programming, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student9, course=arithmetic, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student9, course=prealgebra, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student9, course=basic_geometry, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student9, course=geometric_optics, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student9, course=human_biology, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student9, course=evolution, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student9, course=redox_reactions, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student10, course=arithmetic, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student10, course=prealgebra, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student10, course=basic_geometry, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student10, course=geometric_optics, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student10, course=human_biology, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student10, course=evolution, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student10, course=redox_reactions, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student11, course=arithmetic, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student11, course=prealgebra, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student11, course=basic_geometry, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student11, course=geometric_optics, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student11, course=human_biology, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student11, course=evolution, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student11, course=redox_reactions, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student12, course=arithmetic, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student12, course=prealgebra, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student12, course=basic_geometry, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student12, course=geometric_optics, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student12, course=human_biology, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student12, course=evolution, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student12, course=redox_reactions, enroll_date=date(2015, 9, 3))

    Enrollment.objects.create(user=student13, course=arithmetic, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student13, course=prealgebra, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student13, course=basic_geometry, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student13, course=geometric_optics, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student13, course=human_biology, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student13, course=evolution, enroll_date=date(2015, 9, 3))
    Enrollment.objects.create(user=student13, course=redox_reactions, enroll_date=date(2015, 9, 3))


    assignment_group = AssignmentGroup.objects.create(name="Mandatory")
    assignment_group1 = AssignmentGroup.objects.create(name="Optional")
    assignment = Assignment.objects.create(name="First assignment", description="<i>To be edited</i>", course=machine_learning,
                                           deadline=date(2016, 2, 2), type="PD", group=assignment_group)
    assignment2 = Assignment.objects.create(name="Lab1", description="<b>Statement</b>: Considering a small programming language (that we shall call mini-langauge), you have to write a scanner (lexical analyzer).",
                                            course=compilers, deadline=date(2016,2,2), type="PD", group=assignment_group)
    assignment3 = Assignment.objects.create(name="Lab2", description="<b>Task</b>Starting from syntax rules in BNF notation from Lab 1, construct the context free grammar corresponding to your minilanguage to be used in parsing.",
                                            course=compilers, deadline=date(2016, 2, 16), type="PD", group=assignment_group)

    StudentAssignment.objects.create(user=student, assignment=assignment, grade=0)
    StudentAssignment.objects.create(user=student, assignment=assignment2, grade=0)
    StudentAssignment.objects.create(user=student, assignment=assignment3, grade=0)

    StudentAssignment.objects.create(user=student2, assignment=assignment, grade=0)
    StudentAssignment.objects.create(user=student2, assignment=assignment2, grade=0)
    StudentAssignment.objects.create(user=student2, assignment=assignment3, grade=0)

    # add forums
    create_forums_course(compilers)
    create_forums_course(machine_learning)
    create_forums_course(web_programming)

    create_forums_course(arithmetic)

    create_forums_course(prealgebra)
    create_forums_course(basic_geometry)
    create_forums_course(geometric_optics)
    create_forums_course(human_biology)
    create_forums_course(evolution)
    create_forums_course(redox_reactions)


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

        self.stdout.write("\nLoading example calendar data")
        call_command("load_example_data", verbosity=3, interactive=False)
        call_command("load_sample_data", verbosity=3, interactive=False)

        self.stdout.write("\nInserting data")
        insert_data()

        # self.stdout.write("\nCollecting static files")
        # call_command("collectstatic", verbosity=3, interactive=False)

        self.stdout.write("SUCCESS")
