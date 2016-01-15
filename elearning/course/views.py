#!/usr/bin/python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from elearning.course.forms import SimpleCourseForm, AdminEditCourseForm, TeacherEditCourseForm
from elearning.models import Enrollment, Course, AssistantCourse
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

    return render(request, 'course/add_course.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['admin', 'teacher']).exists())
def see_courses(request):
    user = get_current_user(request)
    user_is_admin = request.user.groups.filter(name='admin').exists()
    can_delete = True if user_is_admin else False
    used_form = AdminEditCourseForm if user_is_admin else TeacherEditCourseForm
    if user_is_admin:
        CourseFormSet = modelformset_factory(Course, fields=('name', 'subject', 'teacher', 'assistants', 'students'),
                                             can_delete=can_delete, form=used_form, max_num=1)
    else:
        CourseFormSet = modelformset_factory(Course, fields=('name', 'subject', 'assistants', 'students'),
                                             can_delete=can_delete, form=used_form, max_num=1)
    if request.method == 'POST':
        formset = CourseFormSet(request.POST, request.FILES)
        if user_is_admin:
            if formset.is_valid():
                for form in formset:
                    course = form.save(commit=False)
                    # TODO get rid of this UGLY WAY
                    Enrollment.objects.filter(course=course).delete()
                    for student in form.clean_students():
                        Enrollment.objects.create(user=student, course=course)
                    AssistantCourse.objects.filter(course=course).delete()
                    for assistant in form.clean_assistants():
                        AssistantCourse.objects.create(user=assistant, course=course)
                    course.save()
                messages.success(request, "Courses successfully edited.")
            else:
                messages.error(request, str(formset.errors))
            return redirect('index')
        else:
            if formset.is_valid():
                for form in formset:
                    course = form.save(commit=False)
                    course.teacher = user
                    Enrollment.objects.filter(course=course).delete()
                    for student in form.clean_students():
                        Enrollment.objects.create(user=student, course=course)
                    AssistantCourse.objects.filter(course=course).delete()
                    for assistant in form.clean_assistants():
                        AssistantCourse.objects.create(user=assistant, course=course)
                    course.save()
                messages.success(request, "Courses successfully edited.")
            else:
                messages.error(request, str(formset.errors))

            return redirect('index')
    else:
        if user_is_admin:
            formset = CourseFormSet(queryset=Course.objects.all())
        else:
            formset = CourseFormSet(queryset=Course.objects.filter(teacher=user))
    return render(request, 'course/see_courses.html', {'formset': formset})
