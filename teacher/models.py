from django.db import models

from accounts.models import Teacher


class Classroom(models.Model):
    class_name = models.CharField(blank=False, max_length=20)
    key = models.CharField(blank=False, max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

#
# class Subject(models.Model):
#     subject_name = models.CharField()
#     classroom = models.ForeignKey()
#
#
# class Homework(models.Model):
#     task = models.TextField()
#     pub_date = models.DateField()
#
#     subject = models.ForeignKey()
#     # mark = models.ForeignKey()
#
#
# class Mark(models.Model):
#     mark = models.CharField()
#     comment = models.TextField()
#     send_date = models.DateField()
#
#     student = models.ForeignKey()
#     homework = models.ForeignKey()