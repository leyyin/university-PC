from django.contrib import admin
from .models import *


@admin.register(UserELearning)
class UserELearningAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone', 'CNP')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')


@admin.register(AssistantCourse)
class AssistantCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'starting_date')



@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enroll_date')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'path')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'lecture_date', 'lecture_index', 'course', 'resource')


@admin.register(AssignmentGroup)
class AssignmentGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'type', 'group')


@admin.register(StudentGroupAssignment)
class StudentGroupAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student_group', 'assignment', 'grade')


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'grade')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_index', 'type')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'time_limit', 'question', 'assignment_group')


@admin.register(StudentTest)
class StudentTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'date_taken', 'grade')


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'thread_date', 'priority')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'user', 'post_date', 'comment')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value')
#