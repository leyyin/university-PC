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

    if request.user.groups.filter(name='student').exists():
        type = 'student'
        enrollments = Enrollment.objects.filter(user=user).all()
        courses = []
        for e in enrollments:
            courses.append((e.course, e.enroll_date))
    elif request.user.groups.filter(name='teacher').exists():
        type = 'teacher'
        courses = Course.objects.filter(teacher=user).all()

    else:
        rc = RequestContext(request, {'type': 'admin'})
        return render(request, 'index.html', context_instance=rc)

    rc = RequestContext(request, {
        "type": type,
        "courses": courses
    })

    return render(request, 'index.html', context_instance=rc)

