from django.db import models
from django.contrib.auth.models import User

class Setting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    def __str__(self):
        return self.course_name
    #def get_course_name(self):
    #    return str(self.course_name)
    def get_period(self):
        return str(self.period)
    def get_course_code(self):
        return self.code
    course_name = models.CharField(max_length=50)
    period = models.IntegerField(default=1) #unused
    code = models.CharField(max_length=9, default="")
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True) #creates relationship between the user and course
    hw = models.TextField(max_length=200, blank=True)


#class Period(models.Model):
#    time = models.IntegerField()
#    hw = models.TextField(max_length=500, blank=True)
#    def __int__(self):
#        return self.time
