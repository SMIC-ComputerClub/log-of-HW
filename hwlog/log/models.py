from martor.models import MartorField
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

class Reminder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #hw_text = models.CharField(max_length=180)
    hw_text = MartorField()
    def __str__(self):
        return self.user.username

class Course(models.Model):
    def __str__(self):
        return self.course_name
    #def get_course_name(self):
    #    return str(self.course_name)
    def get_latest_hw(self):
        latest_hw = self.homework_set.latest('pub_date')
        return latest_hw
    course_name = models.CharField(max_length=50)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True) #creates relationship between the user and course

class Homework(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True)
    #hw_text = models.CharField(max_length=180)
    hw_text = MartorField()
    pub_date = models.DateTimeField('date published')
    poster = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.hw_text

    def was_published_recently(self):
        timenow = timezone.now()
        if ((self.pub_date.weekday()==4 or self.pub_date.weekday()==5) and (timenow.weekday()==5 or timenow.weekday()==6) and (self.pub_date+timedelta(days=3) > timenow)):
            return True #returns true on weekends if hw was posted on friday
        else:
            return self.pub_date.date() == timenow.date()

    def get_pub_date(self):
        return self.pub_date

    def get_poster(self):
        return self.poster

    def get_course(self):
        return self.course
#class Period(models.Model):
#    time = models.IntegerField()
#    hw = models.TextField(max_length=500, blank=True)
#    def __int__(self):
#        return self.time
