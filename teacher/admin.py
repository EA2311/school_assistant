from django.contrib import admin

from teacher.models import Classroom, Subject, Homework, Mark

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Homework)
admin.site.register(Mark)


