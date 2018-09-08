from django import forms
from .models import Course
#from martor.fields import MartorFormField

class ClassEnrollForm(forms.Form): #form to edit course settings
    courseList = Course.objects.order_by('course_name')

    course_1 = forms.ModelChoiceField(queryset=courseList,empty_label=None)
    course_2 = forms.ModelChoiceField(queryset=courseList,empty_label=None)
    course_3 = forms.ModelChoiceField(queryset=courseList,empty_label=None)
    course_4 = forms.ModelChoiceField(queryset=courseList,empty_label=None)
    course_5 = forms.ModelChoiceField(queryset=courseList,empty_label=None)
    course_6 = forms.ModelChoiceField(queryset=courseList,empty_label=None)
    course_7 = forms.ModelChoiceField(queryset=courseList,empty_label=None)

class ChangeHWForm(forms.Form): #form to edit hw of a class
    hw_text = forms.CharField(widget=forms.Textarea(attrs={'maxlength': '300'}))
