from django.db import models

from accounts.models import Teacher


class Classroom(models.Model):
    class_name = models.CharField(blank=False, max_length=20)
    key = models.CharField(blank=False, max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class Homework(models.Model):
    task = models.TextField(max_length=400)
    pub_date = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject} - {self.pub_date}'




# class Mark(models.Model):
#     mark = models.CharField()
#     comment = models.TextField()
#     send_date = models.DateField()
#
#     homework = models.ForeignKey()
