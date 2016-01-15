#!/usr/bin/python
from pybb.models import Category, Forum, Topic

from elearning.models import UserELearning


# Returns the current elearning user
def get_current_user(request):
    return UserELearning.objects.get(user=request.user)


def create_forums_course(course):
    category, exists = Category.objects.get_or_create(name="Courses", slug="courses")

    parent_forum = Forum.objects.create(category=category, name=course.name)
    parent_forum.moderators.add(course.teacher.user)

    # homework forum
    subforums = ["Homework", "Exam", "Off topic"]
    for subforum in subforums:
        Forum.objects.create(category=category, name=subforum, parent=parent_forum)

