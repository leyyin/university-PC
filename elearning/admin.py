from django.contrib import admin
from .models import *


@admin.register(UserELearning)
class UserELearningAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone', 'CNP')
    search_fields = ('address', 'phone', 'CNP')
    list_filter = ('address', 'phone', 'CNP')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')
    list_filter = ('name', 'subject__name')


@admin.register(AssistantCourse)
class AssistantCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'starting_date')
    search_fields = ('user__user__first_name', 'user__user__last_name')
    list_filter = ('user__user__first_name', 'user__user__last_name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enroll_date')
    search_fields = ('user__user__first_name', 'user__user__last_name', 'course__name')
    list_filter = ('user__user__first_name', 'user__user__last_name', 'course__name')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'path')
    search_fields = ('name', 'path')
    list_filter = ('name', 'path')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'lecture_date', 'lecture_index', 'course', 'resource')
    search_fields = ('name', 'course__name')
    list_filter = ('name', 'course__name')


@admin.register(AssignmentGroup)
class AssignmentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'type', 'group')
    search_fields = ('name', 'description', 'group__name')
    list_filter = ('name', 'description', 'group__name')


@admin.register(StudentGroupAssignment)
class StudentGroupAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student_group', 'assignment', 'grade')
    search_fields = ('student_group__name', 'assignment__name', 'grade')
    list_filter = ('student_group__name', 'assignment__name', 'grade')


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'grade')
    search_fields = ('user__user__first_name', 'user__user__last_name', 'assignment__name', 'grade')
    list_filter = ('user__user__first_name', 'user__user__last_name', 'assignment__name', 'grade')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_index', 'type')
    search_fields = ('question_index', 'type')
    list_filter = ('question_index', 'type')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', 'time_limit', 'question', 'assignment_group')
    search_fields = ('name', 'description', 'question__type', 'assignment_group__name')
    list_filter = ('name', 'description', 'question__type', 'assignment_group__name')


@admin.register(StudentTest)
class StudentTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'date_taken', 'grade')
    search_fields = ('user__user__first_name', 'user__user__last_name', 'grade',
                     'test__name', 'test__description', 'test__question__type', 'test__assignment_group__name')
    list_filter = ('user__user__first_name', 'user__user__last_name', 'grade',
                   'test__name', 'test__description', 'test__question__type', 'test__assignment_group__name')


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'thread_date', 'priority')
    search_fields = ('title', 'user__user__first_name', 'user__user__last_name', 'priority__name')
    list_filter = ('title', 'user__user__first_name', 'user__user__last_name', 'priority__name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'user', 'post_date', 'comment')
    search_fields = ('thread__title', 'user__user__first_name', 'user__user__last_name', 'comment')
    list_filter = ('thread__title', 'user__user__first_name', 'user__user__last_name', 'comment')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value')
    search_fields = ('user__user__first_name', 'user__user__last_name', 'post__thread__title', 'value')
    list_filter = ('user__user__first_name', 'user__user__last_name', 'post__thread__title', 'value')
