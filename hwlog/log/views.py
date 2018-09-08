from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .models import Course, Homework, Reminder
from .forms import ClassEnrollForm, ChangeHWForm
from django.utils import timezone
from datetime import datetime, timedelta
import math

def about(request):
    return render(request,'about.html')

def home(request): #index page
    return render(request,'index.html')

def signup(request): #signup page
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() #what does this do
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Reminder.objects.create(user=user)
            login(request, user)
            return redirect('configure')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def change_password(request): #change password page
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def configure(request): #settings page, might be lots of bugs
    if request.method == 'POST':        #what happens if user adds more than 7 courses
        form = ClassEnrollForm(request.POST)
        if form.is_valid():
            request.user.courses_joined.clear()
            coursearray = []
            for x in range(0,7): #adding students to courses
                coursearray.append(form.cleaned_data['course_'+str(x+1)])
                coursearray[x].students.add(request.user)
            return redirect('home')
    else:
        user_courses = request.user.courses_joined.all()
        user_class = [ ]
        no_course = Course.objects.get(course_name='--None--')

        for x in range(0,7): #create an array with user courses^
            if x < len(user_courses):
                user_class.append(user_courses[x])
            else:
                user_class.append(no_course)

        form = ClassEnrollForm(initial={'course_1': user_class[0], #prepopulating with user's settings
                                        'course_2': user_class[1],
                                        'course_3': user_class[2],
                                        'course_4': user_class[3],
                                        'course_5': user_class[4],
                                        'course_6': user_class[5],
                                        'course_7': user_class[6],
                                        })
    return render(request, 'configure.html', {'form': form})

def detail(request, course_id): #page to edit hw
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = ChangeHWForm(request.POST)
        if form.is_valid():
            course.homework_set.create(hw_text=form.cleaned_data['hw_text'], pub_date=timezone.now(), poster=request.user)
            return redirect('home')
    else:
        form = ChangeHWForm()

    one_week_ago = timezone.now()-timedelta(days=7) #create date object to filter homework posted within a week
    hw_list = course.homework_set.filter(pub_date__gte=one_week_ago)
    length = len(hw_list)
    if length > 10: end = length-11
    else: end = None #using 0 doesnt work, since it would exclude the last element
    latest_hw_list = hw_list[length:end:-1]
    if len(course.homework_set.all())-1 >= 0: latest_hw = course.homework_set.all()[len(course.homework_set.all())-1]
    else: latest_hw = ""
    return render(request, 'detail.html', {'form': form,
                                            'course_name': course.course_name,
                                            'course_id': course.id,
                                            'latest_hw_list': latest_hw_list,
                                            'latest_hw': latest_hw})

def history(request, course_id, page): #page to view full history
    course = get_object_or_404(Course, pk=course_id)
    full_list = course.homework_set.all()
    length = len(full_list)
    limit = 30 # how many items per page / doesnt work after 40?
    last_page = math.ceil(length/limit)
    page = int(page)
    if page > last_page:
        return redirect('log:history',course_id=course_id, page=last_page)  
    if (length < limit):
        hw_list = full_list[::-1]
    elif (length-page*limit-1 < limit):
        hw_list = full_list[length-(page-1)*limit-1:0:-1] 
    else:
        hw_list = full_list[length-(page-1)*limit-1:length-page*limit-1:-1]
    prev_bool = True
    next_bool = True
    if page==1: prev_bool = False
    if page==last_page: next_bool = False
    return render(request, 'history.html', {'course_name': course.course_name,
                                            'course_id': course.id,
                                            'prev': prev_bool,
                                            'next': next_bool,
                                            'prev_page':page-1,
                                            'next_page':page+1,
                                            'hw_list': hw_list})


def reminder(request): #page to edit remainder
    if request.method == 'POST':
        form = ChangeHWForm(request.POST)
        if form.is_valid():
            request.user.reminder.hw_text=form.cleaned_data['hw_text']
            request.user.reminder.save()
            return redirect('home')
    else:
        form = ChangeHWForm()

    return render(request, 'reminder.html', {'form': form,})

def game(request):
    return render(request, 'pong.html')