from django import forms
from django.contrib.admin import widgets
from django.db.models.query_utils import Q
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import HiddenInput, Textarea, DateInput
from django.forms import ModelForm, CheckboxSelectMultiple
from django.contrib.auth.models import Group
from elearning.models import Course, Subject,UserELearning, Assignment, AssignmentGroup


# https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/
class SubjectModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class TeacherModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.id+obj.name


class SimpleCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name']
    subject = SubjectModelChoiceField(queryset=Subject.objects.all(), empty_label=None)


class TeacherEditCourseForm(SimpleCourseForm):
    students = forms.ModelMultipleChoiceField(required=False, widget=CheckboxSelectMultiple, queryset=UserELearning.objects.filter(user__groups__name='student'))
    assistants = forms.ModelMultipleChoiceField(required=False, widget=CheckboxSelectMultiple, queryset=UserELearning.objects.filter(user__groups__name='assistant'))

    def clean_students(self):
        data = self.cleaned_data['students']
        return data

    def clean_assistants(self):
        data = self.cleaned_data['assistants']
        return data


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'deadline', 'type', 'group']

        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 7}),
            'deadline': SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                ),
        }
    id = forms.HiddenInput()
    group = forms.ModelChoiceField(required=True, queryset=AssignmentGroup.objects.all(), empty_label=None)


class ReadOnlyAssignmentForm(AssignmentForm):

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['readonly'] = True
            self.fields[key].widget.attrs['disabled'] = 'disabled'
        widgets = {
            'deadline': forms.CharField(),
        }


class AssignStudentsForm(forms.Form):

    def __init__(self, assignment, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields["students"] = forms.ModelMultipleChoiceField(required=False, widget=CheckboxSelectMultiple,
                                              queryset=assignment.course.students.all())

    def clean_students(self):
        data = self.cleaned_data['students']
        return data


class AdminEditCourseForm(TeacherEditCourseForm):
    teacher = forms.ModelChoiceField(required=True, queryset=UserELearning.objects.filter(user__groups__name='teacher'), empty_label=None)

