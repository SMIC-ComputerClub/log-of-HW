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
            #course_1 = form.cleaned_data['course_1']
            #course_1.students.add(request.user)
            #course_2 = form.cleaned_data['course_2']
            #course_2.students.add(request.user)
            #course_3 = form.cleaned_data['course_3']
            #course_3.students.add(request.user)
            #course_4 = form.cleaned_data['course_4']
            #course_4.students.add(request.user)
            #course_5 = form.cleaned_data['course_5']
            #course_5.students.add(request.user)
            #course_6 = form.cleaned_data['course_6']
            #course_6.students.add(request.user)
            #course_7 = form.cleaned_data['course_7']
            #course_7.students.add(request.user)
            return redirect('home')
    else:
        user_courses = request.user.courses_joined.all()
        user_class = [ ]
        no_course = Course.objects.get(course_name='--None--')

    #    try:                                                        #extremely inefficient i think
    #        user_class_1 = user_courses[0]
    #    except IndexError:
    #        user_class_1 = no_course
    #    try:
    #        user_class_2 = user_courses[1]
    #    except IndexError:
    #        user_class_2 = no_course
    #    try:
    #        user_class_3 = user_courses[2]
    #    except IndexError:
    #        user_class_3 = no_course
    #    try:
    #        user_class_4 =user_courses[3]
    #    except IndexError:
    #        user_class_4 = no_course
    #    try:
    #        user_class_5 = user_courses[4]
    #    except IndexError:
    #        user_class_5 = no_course
    #    try:
    #        user_class_6 = user_courses[5]
    #    except IndexError:
    #        user_class_6 = no_course
    #    try:
    #        user_class_7 = user_courses[6]
    #    except IndexError:
    #        user_class_7 = no_course
        for x in range(0,7):                    #loop to do the same thing as that^
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
    return render(request, 'detail.html', {'form': form,
                                            'course': course,
                                            'latest_hw_list': course.homework_set.order_by('-pub_date')[:5]})
