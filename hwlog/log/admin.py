from django.contrib import admin

# Register your models here.
from .models import Course, Homework
#from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.contrib.admin.models import LogEntry
from django.contrib.admin.widgets import FilteredSelectMultiple




class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['course_name','students']}),
    ]
    filter_horizontal = ['students']
    inlines = [HomeworkInline]
    #filter_horizontal = ['students']
#    list_display = ('question_text','pub_date','was_published_recently')
#    list_filter = ['pub_date']
#    search_fields = ['question_text']

#class CustomUserAdmin(admin.ModelAdmin):
#    fieldsets = (
#        (None, {'fields': ('username', 'password')}),
#        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                       'groups', 'user_permissions')}),
#        (('Important dates'), {'fields': ('last_login', 'date_joined',)}),
#    )

    #inlines = [CourseInline]
    #filter_horizontal = ['courses_joined'] #how to make this work?


class HomeworkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['hw_text','course','pub_date']}),
    ]

#admin.site.unregister(User)
#admin.site.register(User, CustomUserAdmin)

admin.site.register(LogEntry)

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Course, CourseAdmin)
