from django.db import models
from django.contrib.auth.models import User


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


class Subject(models.Model):
    name = models.CharField(max_length=64)


class Course(models.Model):
    name = models.CharField(max_length=64)
    subject = models.ForeignKey(Subject)
    users = models.ManyToManyField(User, through="Enrollment")


class Enrollment(models.Model):
    user = models.ForeignKey(User)
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


class Assignment(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    deadline = models.DateField()


class Delivery(models.Model):
    type = models.CharField(max_length=128)


class UserAssignment(models.Model):
    user = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    delivery = models.ForeignKey(Delivery)

    class Meta:
        unique_together = (('user', 'assignment'),)


class Question(models.Model):
    question_index = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=128)


class Test(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    deadline = models.DateField()
    question = models.ForeignKey(Question)


class UserTest(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    date_taken = models.DateField()

    class Meta:
        unique_together = (('user', 'test'),)


class Group(models.Model):
    name = models.CharField(max_length=128)


class UserGroup(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)

    class Meta:
        unique_together = (('user', 'group'),)


class Priority(models.Model):
    name = models.CharField(max_length=128)


class Thread(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    thread_date = models.DateField()
    priority = models.ForeignKey(Priority)


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)
    post_date = models.DateField()
    comment = models.CharField(max_length=1024)


class Rating(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    value = models.IntegerField()

    class Meta:
        unique_together = (('user', 'post'),)

