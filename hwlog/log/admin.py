from django.contrib import admin

# Register your models here.
from .models import Course, Period

class PeriodInline(admin.TabularInline):
    model = Period
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['course_name']}),
        (None,               {'fields': ['code']}),
    ]
    inlines = [PeriodInline]
#    list_display = ('question_text','pub_date','was_published_recently')
#    list_filter = ['pub_date']
#    search_fields = ['question_text']

admin.site.register(Course, CourseAdmin)
