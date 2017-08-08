from django import forms
from .models import Course

class ClassEnrollForm(forms.Form):
    course_1 = forms.ModelChoiceField(queryset=Course.objects.all())
    course_2 = forms.ModelChoiceField(queryset=Course.objects.all())
    course_3 = forms.ModelChoiceField(queryset=Course.objects.all())
    course_4 = forms.ModelChoiceField(queryset=Course.objects.all())
    course_5 = forms.ModelChoiceField(queryset=Course.objects.all())
    course_6 = forms.ModelChoiceField(queryset=Course.objects.all())
    course_7 = forms.ModelChoiceField(queryset=Course.objects.all())
