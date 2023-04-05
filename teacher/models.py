from django.db import models

from accounts.models import Teacher


def classroom_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"teacher_{instance.teacher.user.id}/{instance.class_name}.{ext}"
    return filename


class Classroom(models.Model):
    class_name = models.CharField(blank=False, max_length=20)
    key = models.CharField(blank=False, max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=classroom_file_name)

    def __str__(self):
        return self.class_name


def subject_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"teacher_{instance.classroom.class_name}/{instance.subject_name}.{ext}"
    return filename


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=subject_file_name, default='placeholder_image.webp')

    def __str__(self):
        return self.subject_name


class HomeTask(models.Model):
    task = models.TextField(max_length=400)
    pub_date = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task} - {self.pub_date}'


def ht_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"teacher_{instance.home_task.subject.classroom.teacher.user.id}/{instance.home_task.subject.subject_name}/{instance.home_task.pub_date}.{ext}"
    return filename


class ImagesHT(models.Model):
    image = models.ImageField(upload_to=ht_file_name, null=False, blank=False)
    home_task = models.ForeignKey(HomeTask, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.image} - {self.home_task}'


class Mark(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    homework = models.OneToOneField('student.StudentWork', on_delete=models.CASCADE)

    mark = models.CharField(max_length=50)
    comment = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.teacher.user.first_name} - {self.mark}'
