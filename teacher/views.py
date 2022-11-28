from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView

from accounts.models import Teacher
from teacher.forms import ClassroomCreateForm
from teacher.models import Classroom, Subject


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


class CreateClassroomsView(CreateView):
    template_name = 'teacher/create_classroom.html'
    form_class = ClassroomCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.key = 122 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        self.object.teacher = teacher
        self.object.save()
        return redirect('teacher:classrooms')


class DetailClassroomView(DetailView):
    model = Classroom
    template_name = 'teacher/classroom_detail.html'
    context_object_name = 'classroom'


class SubjectsView(ListView):
    template_name = 'teacher/subjects.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        classroom = Classroom.objects.get(id=self.request.GET('pk'))
        subjects = Subject.objects.filter(classroom=classroom)
        return subjects
