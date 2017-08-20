from django.contrib import admin

# Register your models here.
from .models import Course, Homework

class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['course_name','code','students']}),
    ]
    inlines = [HomeworkInline]
    #filter_horizontal = ['students']
#    list_display = ('question_text','pub_date','was_published_recently')
#    list_filter = ['pub_date']
#    search_fields = ['question_text']

admin.site.register(Course, CourseAdmin)
