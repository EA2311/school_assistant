from django.contrib import admin

from teacher.models import Classroom, Subject, Homework


admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Homework)

