#!/usr/bin/python
from elearning.models import UserELearning


# Returns the current elearning user
def get_current_user(request):
    return UserELearning.objects.get(user=request.user)
