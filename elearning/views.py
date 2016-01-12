#!/usr/bin/python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.context import RequestContext

from elearning.course.forms import AddCourseForm
from elearning.models import Enrollment, UserELearning, Course


@login_required
def index(request):
    user_elearning = UserELearning.objects.get(user=request.user)
    if request.user.groups.filter(name='student').exists():
        type = 'student'
        enrollments = Enrollment.objects.filter(user=user_elearning).all()
        courses = []
        for e in enrollments:
            courses.append((e.course, e.enroll_date))
    elif request.user.groups.filter(name='teacher').exists():
        type = 'teacher'
        courses = Course.objects.filter(teacher=user_elearning).all()

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
        user_elearning = UserELearning.objects.get(user=request.user)
        form = AddCourseForm(request.POST)
        if form.is_valid():
            query = Course.objects.create(name=form.cleaned_data['name'], subject=form.cleaned_data['subject'],
                                          teacher=user_elearning)
            print(query)

    else:
        form = AddCourseForm()
    return render(request, 'course/add_course.html', {'form': form.as_table()})
