from django.db import models

from accounts.models import Student
from teacher.models import HomeTask


class StudentWork(models.Model):
    home_task = models.ForeignKey(HomeTask, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    send_date = models.DateTimeField(auto_now_add=True)

    text = models.TextField()
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.home_task.subject} - {self.home_task} - {self.student}'


def sw_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"homework_images/student_{instance.work.student.user.id}/{instance.work.home_task.subject.subject_name}\
    /{instance.work.send_date}.{ext} "
    return filename


class ImagesSW(models.Model):
    image = models.ImageField(upload_to=sw_file_name, null=False, blank=False)
    work = models.ForeignKey(StudentWork, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.image} - {self.work}'
