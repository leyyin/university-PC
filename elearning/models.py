from django.db import models
from django.contrib.auth.models import User


# TODO find if needed
class UserELearning(models.Model):
    user = models.OneToOneField(User)


class Subject(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        permissions = (
            ("read_car", "Can read Car"),
        )

