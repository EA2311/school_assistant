from django.db import models
from accounts.models import Teacher
from managers import NoneManager
from teacher.services.models_services import get_random_string, generate_file_name


class Classroom(models.Model):
    class_name = models.CharField(blank=False, max_length=20)
    key = models.CharField(blank=False, max_length=50, unique=True, default=get_random_string)
    image = models.ImageField(upload_to=generate_file_name)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=generate_file_name, default='placeholder_image.webp')

    def __str__(self):
        return self.subject_name


class HomeTask(models.Model):
    task = models.TextField(max_length=400)
    pub_date = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task} - {self.pub_date}'


class ImagesHT(models.Model):
    objects = NoneManager()

    image = models.ImageField(upload_to=generate_file_name, null=False, blank=False)
    home_task = models.ForeignKey(HomeTask, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.image} - {self.home_task}'


class Mark(models.Model):
    objects = NoneManager()

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    homework = models.OneToOneField('student.StudentWork', on_delete=models.CASCADE)

    mark = models.CharField(max_length=50)
    comment = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.teacher.user.first_name} - {self.mark}'
