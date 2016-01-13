from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple
from django.contrib.auth.models import Group
from elearning.models import Course, Subject,UserELearning


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


class AdminEditCourseForm(TeacherEditCourseForm):
    teacher = forms.ModelChoiceField(required=True, queryset=UserELearning.objects.filter(user__groups__name='teacher'), empty_label=None)

