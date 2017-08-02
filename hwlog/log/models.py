from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    code = models.CharField(max_length=9, default="*")
    def __str__(self):
        return self.course_name
    def get_course_code(self):
        return code

class Period(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time = models.IntegerField()
    hw = models.TextField(max_length=500, blank=True)
    def __int__(self):
        return self.time
