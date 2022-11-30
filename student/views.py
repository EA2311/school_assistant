from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.models import Student
from teacher.models import Classroom, Subject, Homework


class StudentClassroomView(View):

    def get(self, request):
        student = Student.objects.get(user=request.user)
        if student.classroom:
            subjects = Subject.objects.filter(classroom=student.classroom)
            context = {"student": student, "subjects": subjects}
        else:
            context = {"student": student}
        return render(request, "student/student_subjects.html", context)

    def post(self, request):
        student = Student.objects.get(user=request.user)
        print(request.POST.get("key"))
        classroom = Classroom.objects.get(key=request.POST.get("key"))
        student.classroom = classroom
        student.save()
        return redirect('student:student_classrooms')


class StudentHomeworksView(ListView):
    template_name = 'student/student_homeworks.html'
    context_object_name = 'home_tasks'

    def get_queryset(self):
        subject = Subject.objects.get(id=self.kwargs['subj'])
        home_tasks = Homework.objects.filter(subject=subject)
        return home_tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(id=self.kwargs['subj'])
        context['subject'] = subject
        context['student'] = self.request.user

        return context


class StudentDetailHomeworkView(DetailView):
    model = Homework
    template_name = 'student/detail_home_tasks.html'
    context_object_name = 'home_task'


def send(request, subj, pk):
    try:
        print(request.POST['hw'])
    except (KeyError):
        print('error')

    return HttpResponseRedirect(reverse('student:detail_home_tasks', args=(subj, pk,)))
