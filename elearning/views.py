#!/usr/bin/python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.context import RequestContext

from elearning.course.forms import AddCourseForm
from elearning.models import Enrollment, UserELearning, Course


# Returns the current elearning user
def get_current_user(request):
    return UserELearning.objects.get(user=request.user)


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


@login_required
def add_course(request):
    if request.method == 'POST':
        user = get_current_user(request)
        form = AddCourseForm(request.POST)
        if form.is_valid():
            Course.objects.create(name=form.cleaned_data['name'], subject=form.cleaned_data['subject'],
                                  teacher=user)
            messages.success(request, "Course created")
            return redirect('index')
    else:
        form = AddCourseForm()

    return render(request, 'course/add_course.html', {'form': form})
