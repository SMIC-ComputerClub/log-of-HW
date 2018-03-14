from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .models import Course
from .forms import ClassEnrollForm, ChangeHWForm
from .models import Homework
from django.utils import timezone
from datetime import datetime, timedelta

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
            try:
                user_class.append(user_courses[x])
            except IndexError:
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
        form = ChangeHWForm({'hw':course.get_latest_hw})

    one_week_ago = timezone.now()-timedelta(days=7) #create date object to filter homework posted within a week
    return render(request, 'detail.html', {'form': form,
                                            'course': course,
                                            'latest_hw_list': course.homework_set.filter(pub_date__gte=one_week_ago).reverse()})
