from django import forms
from django.forms import ModelForm
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


class AdminEditCourseForm(SimpleCourseForm):

    # students = forms.MultipleChoiceField()
    class Meta(SimpleCourseForm.Meta):
        include = ('teacher','students',)
    # teacher = forms.ModelMultipleChoiceField(queryset=Group.objects.get('teacher').user_set.all(), empty_label=None)
    # teacher = forms.ModelMultipleChoiceField(queryset=UserELearning.objects.all())