#!/usr/bin/python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.db.models import Q

from elearning.course.forms import SimpleCourseForm, AdminEditCourseForm, TeacherEditCourseForm, AssignmentForm, \
    ReadOnlyAssignmentForm, AssignStudentsForm
from elearning.models import Enrollment, UserELearning, Course, AssistantCourse, Assignment, StudentAssignment
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
@user_passes_test(lambda u: u.groups.filter(name__in=['assistant', 'teacher']).exists())
def add_assignment(request, id):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = Course.objects.get(id=id)
            assignment.save()
            messages.success(request, "Assignment created")
        else:
            messages.error(request, "Assignment not created")
        return redirect('index')
    else:
        course = Course.objects.get(id=id)
        user = get_current_user(request)
        if course.teacher != user and user not in course.assistants.all():
            messages.error(request, "You are not allowed to add an assignment to this course.")
            return redirect('index')
        form = AssignmentForm()
        return render(request, 'course/add_assignment.html', {'form': form,'course': course})


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


@login_required
def see_assignments(request, id):
    user = get_current_user(request)
    course = Course.objects.get(id=id)
    can_delete = True if user == course.teacher or user in course.assistants.all() else False
    AssignmentFormSet = modelformset_factory(Assignment, fields=('id', 'name', 'description', 'deadline', 'type', 'group'), can_delete=can_delete, form=AssignmentForm, max_num=0)
    if request.method == 'POST':
        formset = AssignmentFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            messages.success(request,"Assignments successfully saved.")
        return redirect('index')
    else:
        if user.is_in_group("student"):
            AssignmentFormSet.form = ReadOnlyAssignmentForm
            formset = AssignmentFormSet(queryset=Assignment.objects.filter(Q(students__user=request.user) and
                                                                           Q(course=course)).all())
        else:
            formset = AssignmentFormSet(queryset=Assignment.objects.filter(course=course).all())
    if len(formset) == 0:
        messages.info(request, "There are no assignments for this course")
        return redirect('index')
    else:
        return render(request, 'course/see_assignments.html', {'formset': formset, 'course': course, 'user_elearning': user})


@login_required()
def give_assignment_to_students(request, assignment_id):
    if request.method == "POST":
        assignment = Assignment.objects.get(id=assignment_id)
        form = AssignStudentsForm(assignment, request.POST, request.FILES)
        if form.is_valid():
            for student in form.clean_students():
                StudentAssignment.objects.get_or_create(user=student, assignment= assignment, grade = 0)
            messages.success(request, "Assignment successfully given.")
            return redirect('index')
    else:
        assignment = Assignment.objects.get(id=assignment_id)
        form = AssignStudentsForm(assignment)
    return render(request, 'course/give_assignment_to_students.html', {'form': form,'id':assignment_id})


# TODO
@login_required()
def give_assignment_to_groups(request, assignment_id):
    if request.method == "POST":
        pass
    else:
        messages.info(request, 'There are no available groups.')
    return redirect('index')
