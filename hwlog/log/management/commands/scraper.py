from django.core.management.base import BaseCommand
from log.models import Homework, Course
from django.contrib.auth.models import User
import csv

# python manage.py scraper [filename] [0-2]

class Command(BaseCommand):
    help = 'Scrapes homework data'
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='File name of saved file')
        parser.add_argument('option', type=int, help='Scraping option (0 to 2)')

    def handle(self, *args, **kwargs):

        filename = kwargs['filename']
        if (not filename.endswith(".csv")):
            filename+=".csv"
        csvfile = open(filename, "w")
        csvwriter = csv.writer(csvfile)
        
        option = kwargs['option']
        if (option==0):
           all_homework = Homework.objects.all()
           for hw in all_homework:
                course = hw.get_course()
                pub_date = hw.get_pub_date()
                poster = hw.get_poster()
                csvwriter.writerow([course, poster, pub_date])
        elif (option==1):
            all_courses = Course.objects.all()
            for course in all_courses:
                course_name = course
                hw_count = course.homework_set.count()
                user_count = course.students.count() #lol i thought it was course.user_set 
                csvwriter.writerow([course_name, hw_count, user_count]) 
        elif (option==2):
            all_users = User.objects.all()
            for user in all_users:
                name = user.get_username()
                hw_post_count = user.homework_set.count()
                csvwriter.writerow([name, hw_post_count])

