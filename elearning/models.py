from django.db import models
from django.contrib.auth.models import User


class UserELearning(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    CNP = models.CharField(max_length=13)


class Subject(models.Model):
    name = models.CharField(max_length=64)

