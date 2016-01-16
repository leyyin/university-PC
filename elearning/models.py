from django.contrib.auth.models import User, Group
from django.db import models
from pybb.models import Forum


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

    def is_admin(self):
        return self.is_in_group("admin")

    def is_teacher(self):
        return self.is_in_group("teacher")

    def is_assistant(self):
        return self.is_in_group("assistant")

    def is_student(self):
        return self.is_in_group("student")

    def is_in_group(self, group_name):
        return self.user.groups.filter(name=group_name).exists()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Subject(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=64)
    subject = models.ForeignKey(Subject)
    students = models.ManyToManyField(UserELearning, related_name="student_course", through="Enrollment")
    teacher = models.ForeignKey(UserELearning, related_name="teacher_course")
    assistants = models.ManyToManyField(UserELearning, related_name="assistant_course", through="AssistantCourse")

    def get_forum_id(self):
        return Forum.objects.get(name=self.name).id

    def __str__(self):
        return '{0} | {1}'.format(self.name, self.subject.name)


# Intermediary model that manage the many-to-many relationship between Assistant and Course
class AssistantCourse(models.Model):
    user = models.ForeignKey(UserELearning)
    course = models.ForeignKey(Course)
    starting_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (('user', 'course'),)


class Enrollment(models.Model):
    user = models.ForeignKey(UserELearning)
    course = models.ForeignKey(Course)
    enroll_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (('user', 'course'),)

    def __str__(self):
        return '{0} | {1}'.format(self.user.user.username, self.course.name)


class Resource(models.Model):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=256)

    def __str__(self):
        return '{0} | {1}'.format(self.name, self.path)


class Lecture(models.Model):
    name = models.CharField(max_length=64)
    lecture_date = models.DateField()
    lecture_index = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course)
    resource = models.ForeignKey(Resource)

    def __str__(self):
        return '{0} | {1} | {2}'.format(self.name, self.course.name, self.resource.name)


# Model for grouping the assignments
class AssignmentGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Model for grouping the students
class StudentGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


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
    course = models.ForeignKey(Course)
    deadline = models.DateField()
    type = models.CharField(max_length=2, choices=ASSIGNMENT_TYPES)
    students = models.ManyToManyField(UserELearning, through="StudentAssignment")
    group = models.ForeignKey(AssignmentGroup, blank=True)

    def __str__(self):
        return '{0} | {1} | {2} | {3}'.format(self.name, self.description, self.type, self.group)


# Intermediary model that manage the many-to-many relationship between Assignment and StudentGroup
class StudentGroupAssignment(models.Model):
    student_group = models.ForeignKey(StudentGroup)
    assignment = models.ForeignKey(Assignment)
    grade = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('student_group', 'assignment'),)

    def __str__(self):
        return '{0}'.format(self.student_group)


# Intermediary model that manage the many-to-many relationship between Assignment and Student
class StudentAssignment(models.Model):
    user = models.ForeignKey(UserELearning)
    assignment = models.ForeignKey(Assignment)
    grade = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'assignment'),)

    def __str__(self):
        return '{0} | {1}'.format(self.user.user.username, self.assignment.name)


class Question(models.Model):
    question_index = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=128)

    def __str__(self):
        return '{0}'.format(self.type)


class Test(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    deadline = models.DateField()
    time_limit = models.PositiveSmallIntegerField()
    question = models.ForeignKey(Question)
    students = models.ManyToManyField(UserELearning, through="StudentTest")
    assignment_group = models.ForeignKey(AssignmentGroup)

    def __str__(self):
        return '{0} | {1} | {2} | {3}'.format(self.name, self.description, self.question, self.assignment_group)


# Intermediary model that manage the many-to-many relationship between Student and Test
class StudentTest(models.Model):
    user = models.ForeignKey(UserELearning)
    test = models.ForeignKey(Test)
    date_taken = models.DateField()
    grade = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('user', 'test'),)

    def __str__(self):
        return '{0} | {1}'.format(self.user.user.username, self.test.name)


class Priority(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Thread(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(UserELearning)
    thread_date = models.DateField(auto_now=True)
    priority = models.ForeignKey(Priority)

    def __str__(self):
        return '{0} | {1}'.format(self.title, self.user.user.username)


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(UserELearning)
    post_date = models.DateField(auto_now=True)
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return '{0} | {1} | {2}'.format(self.thread.title, self.user.user.username, self.comment)


class Rating(models.Model):
    user = models.ForeignKey(UserELearning)
    post = models.ForeignKey(Post)
    value = models.IntegerField()

    class Meta:
        unique_together = (('user', 'post'),)

    def __str__(self):
        return '{0} | {1}'.format( self.user.user.username, self.post)
