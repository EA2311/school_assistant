from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import Teacher
from teacher.models import Classroom


class ClassroomsView(ListView):
    template_name = 'teacher/classrooms.html'
    context_object_name = 'classrooms'

    # def get(self, request):
    #     teacher = Teacher.objects.get(user=self.request.user)
    #     classrooms = Classroom.objects.filter(teacher=teacher)
    #     context = {"classrooms": classrooms}
    #     return render(request, "classrooms.html", context)

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        classrooms = Classroom.objects.filter(teacher=teacher)
        return classrooms
