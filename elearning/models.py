from django.contrib.auth.models import User, Group
from django.db import models


class UserELearningManager(models.Manager):
    def create_user(self, username, email, password, first_name=None, last_name=None, address=None, phone=None,
                    cnp=None):
        user = User.objects.create_user(username=username, email=email, password=password, last_name=last_name,
                                        first_name=first_name)

        user_elearning = self.model(user=user, address=address, phone=phone, CNP=cnp)
        user_elearning.save(using=self._db)

        return user_elearning


class UserELearning(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=64, null=True)
    phone = models.CharField(max_length=16, null=True)
    CNP = models.CharField(max_length=13, null=True)
    objects = UserELearningManager()

    def add_to_group(self, name):
        group = Group.objects.get(name=name)
        self.user.groups.add(group)

    def grant_admin_rights(self):
        self.add_to_group("admin")
        self.user.is_staff = True
        # TODO custom specify model permissions
        self.user.is_superuser = True
        self.user.save()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Subject(models.Model):
    name = models.CharField(max_length=64)


class Course(models.Model):
    name = models.CharField(max_length=64)
    subject = models.ForeignKey(Subject)
    students = models.ManyToManyField(UserELearning, related_name="student_course", through="Enrollment")
    teacher = models.ForeignKey(UserELearning, related_name="teacher_course")
    assistants = models.ManyToManyField(UserELearning, related_name="assistant_course", through="AssistantCourse")

    # TODO: write all the __str__ functions

    def __str__(self):
        return '[Name:' + self.name + ';Subject:' + self.subject.name + ']'


# Intermediary model that manage the many-to-many relationship between Assistant and Course
class AssistantCourse(models.Model):
    user = models.ForeignKey(UserELearning)
    course = models.ForeignKey(Course)
    starting_date = models.DateField()

    class Meta:
        unique_together = (('user', 'course'),)


class Enrollment(models.Model):
    user = models.ForeignKey(UserELearning)
    course = models.ForeignKey(Course)
    enroll_date = models.DateField()

    class Meta:
        unique_together = (('user', 'course'),)


class Resource(models.Model):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=256)


class Lecture(models.Model):
    name = models.CharField(max_length=64)
    lecture_date = models.DateField()
    lecture_index = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course)
    resource = models.ForeignKey(Resource)


# Model for grouping the assignments
class AssignmentGroup(models.Model):
    name = models.CharField(max_length=64)


# Model for grouping the students
class StudentGroup(models.Model):
    name = models.CharField(max_length=64)


# An assignment has a type, can be linked to a student or to a group of students
# and has an AssignmentGroup
class Assignment(models.Model):
    ASSIGNMENT_TYPES = (
        ("PD", "Physical Delivery"),  # Predare in format fizic
        ("ND", "No Delivery"),  # Fara predare
        ("UD", "Upload Delivery"),  # Cu incarcare fisiere
        ("LD", "Link Delivery"),  # Ca si legatura(link, url)
        ("FA", "Fill-in Assignment"),  # Cu completare text
        ("GA", "Group Assignment")
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    deadline = models.DateField()
    type = models.CharField(max_length=2, choices=ASSIGNMENT_TYPES)
    students = models.ManyToManyField(UserELearning, through="StudentAssignment")
    group = models.ForeignKey(AssignmentGroup)


# Intermediary model that manage the many-to-many relationship between Assignment and StudentGroup
class StudentGroupAssignment(models.Model):
    student_group = models.ForeignKey(StudentGroup)
    assignment = models.ForeignKey(Assignment)
    grade = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('student_group', 'assignment'),)


# Intermediary model that manage the many-to-many relationship between Assignment and Student
class StudentAssignment(models.Model):
    user = models.ForeignKey(UserELearning)
    assignment = models.ForeignKey(Assignment)
    grade = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'assignment'),)


class Question(models.Model):
    question_index = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=128)


class Test(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    deadline = models.DateField()
    time_limit = models.PositiveSmallIntegerField()
    question = models.ForeignKey(Question)
    students = models.ManyToManyField(UserELearning, through="StudentTest")
    assignment_group = models.ForeignKey(AssignmentGroup)


# Intermediary model that manage the many-to-many relationship between Student and Test
class StudentTest(models.Model):
    user = models.ForeignKey(UserELearning)
    test = models.ForeignKey(Test)
    date_taken = models.DateField()
    grade = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'test'),)


class Priority(models.Model):
    name = models.CharField(max_length=128)


class Thread(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(UserELearning)
    thread_date = models.DateField()
    priority = models.ForeignKey(Priority)


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(UserELearning)
    post_date = models.DateField()
    comment = models.CharField(max_length=1024)


class Rating(models.Model):
    user = models.ForeignKey(UserELearning)
    post = models.ForeignKey(Post)
    value = models.IntegerField()

    class Meta:
        unique_together = (('user', 'post'),)
