#!/usr/bin/python
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from elearning.models import Enrollment, UserELearning


@login_required
def index(request):
    user_elearning = UserELearning.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(user=user_elearning).all()
    courses = []
    for e in enrollments:
        courses.append((e.course, e.enroll_date))
    rc = RequestContext(request,{
        "type": "student",
        "courses": courses
    })
    return render(request, 'index.html', context_instance=rc)
