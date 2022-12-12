from django.db import models

from accounts.models import Student
from teacher.models import HomeTask


class StudentWork(models.Model):
    home_task = models.ForeignKey(HomeTask, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    send_date = models.DateTimeField(auto_now_add=True)

    text = models.TextField()
    image = models.ImageField(upload_to='homework_images')
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.home_task.subject} - {self.home_task} - {self.student}'

