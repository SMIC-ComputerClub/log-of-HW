from django import forms
from .models import Course

class ClassEnrollForm(forms.Form): #form to edit course settings
    course_1 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))
    course_2 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))
    course_3 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))
    course_4 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))
    course_5 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))
    course_6 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))
    course_7 = forms.ModelChoiceField(queryset=Course.objects.all(), initial=Course.objects.get(course_name='None'))

class ChangeHWForm(forms.Form): #form to edit hw of a class
    hw_text = forms.CharField(widget=forms.Textarea(attrs={'maxlength': '200'}))
