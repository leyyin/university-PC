#!/usr/bin/python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.context import RequestContext


from elearning.models import Enrollment, UserELearning, Course
from elearning.utils import get_current_user



@login_required
def index(request):
    user = get_current_user(request)

    if user.is_student():
        courses = Course.objects.filter(students__user=request.user).all()
        # enrollments = Enrollment.objects.filter(user=user).all()
        # courses = []
        # for e in enrollments:
        #     courses.append((e.course, e.enroll_date))
    elif user.is_teacher():
        courses = Course.objects.filter(teacher=user).all()
    elif user.is_assistant():
        courses = Course.objects.filter(assistants__user=request.user).all()
    else:
        courses = Course.objects.all()

    rc = RequestContext(request, {
        "user_elearning": user,
        "courses": courses
    })
    return render(request, 'index.html', context_instance=rc)

