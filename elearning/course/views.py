#!/usr/bin/python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory

from elearning.course.forms import SimpleCourseForm, AdminEditCourseForm
from elearning.models import Enrollment, UserELearning, Course
from elearning.utils import get_current_user


@login_required
def add_course(request):
    if request.method == 'POST':
        user = get_current_user(request)
        form = SimpleCourseForm(request.POST)
        if form.is_valid():
            Course.objects.create(name=form.cleaned_data['name'], subject=form.cleaned_data['subject'],
                                  teacher=user)
            messages.success(request, "Course created")
            return redirect('index')
    else:
        form = SimpleCourseForm()

    return render(request, 'course/add_course.html', {'form': form.as_table()})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['admin', 'teacher']).exists())
def see_courses(request):
    user = get_current_user(request)
    user_is_admin = request.user.groups.filter(name='admin').exists()
    can_delete = True if user_is_admin else False
    used_form = AdminEditCourseForm if user_is_admin else SimpleCourseForm
    if user_is_admin:
        CourseFormSet = modelformset_factory(Course, fields=('name', 'subject',"teacher","students"), can_delete=can_delete, form=used_form, max_num=1)
    else:
        CourseFormSet = modelformset_factory(Course, fields=('name', 'subject'), can_delete=can_delete, form=used_form, max_num=1)
    if request.method == 'POST':
        formset = CourseFormSet(request.POST, request.FILES)
        if user_is_admin:
            if formset.is_valid():
                formset.save()
            else:
                messages.error(request, "ERROR" + formset.errors.__str__())
        else:
            if formset.is_valid():
                for form in formset:
                    course = form.save(commit=False)
                    course.teacher = user
                    course.save()
                messages.success(request, "Courses successfully edited.")
            else:
                messages.error(request, "ERROR" + formset.errors.__str__())

            return redirect('index')
    else:
        if user_is_admin:
            formset = CourseFormSet(queryset=Course.objects.all())
        else:
            formset = CourseFormSet(queryset=Course.objects.filter(teacher=user))


    return render(request, 'course/see_courses.html', {'formset': formset})
