from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView

from accounts.models import Teacher
from teacher.forms import ClassroomCreateForm, SubjectCreateForm
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
        classroom = Classroom.objects.get(id=self.kwargs['pk'])
        subjects = Subject.objects.filter(classroom=classroom)
        return subjects

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['pk'] = self.kwargs['pk']
        return context


class CreateSubjectView(CreateView):
    template_name = 'teacher/create_subjects.html'
    form_class = SubjectCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        classroom = Classroom.objects.get(id=self.kwargs['pk'])
        self.object.classroom = classroom
        self.object.save()
        return redirect('teacher:subjects', pk=self.kwargs['pk'])
