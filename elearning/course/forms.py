from django.forms import ModelForm
from django import forms
from elearning.models import Course, Subject


class AddCourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['name']

    class SubjectModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.name

    subject = SubjectModelChoiceField(queryset=Subject.objects.all(), empty_label=None)

