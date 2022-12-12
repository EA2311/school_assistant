import random

from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required
from accounts.models import Teacher, Student
from student.models import StudentWork
from teacher.forms import ClassroomCreateForm, SubjectCreateForm, HomeworkCreateForm
from teacher.models import Classroom, Subject, HomeTask, ImagesHT


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassroomsView(ListView):
    template_name = 'teacher/classrooms.html'
    context_object_name = 'classrooms'

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        classrooms = Classroom.objects.filter(teacher=teacher)
        return classrooms


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassroomDeleteView(DeleteView):
    success_url = reverse_lazy('teacher:classrooms')
    model = Classroom

    def get(self, *a, **kw):
        return self.delete(*a, **kw)


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateClassroomsView(CreateView):
    template_name = 'teacher/create_classroom.html'
    form_class = ClassroomCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.key = random.randint(100000, 999999)
        self.object.teacher = teacher
        self.object.save()
        return redirect('teacher:classrooms')


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassroomUpdateView(UpdateView):
    model = Classroom
    fields = ['class_name', 'key', 'image']
    template_name = 'teacher/classroom_update.html'
    success_url = reverse_lazy('teacher:classrooms')


@method_decorator([login_required, teacher_required], name='dispatch')
class DetailClassroomView(DetailView):
    model = Classroom
    template_name = 'teacher/classroom_detail.html'
    context_object_name = 'classroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = Classroom.objects.get(id=self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        students = Student.objects.filter(classroom=classroom).order_by('user__last_name')
        unchecked = Count('studentwork', filter=Q(studentwork__is_checked=False))
        students = students.annotate(unchecked=unchecked)
        context['students'] = students
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectsView(ListView):
    template_name = 'teacher/subjects.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        classroom = Classroom.objects.get(id=self.kwargs['pk'])
        subjects = Subject.objects.filter(classroom=classroom)
        return subjects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        classroom = Classroom.objects.get(id=self.kwargs['pk'])
        context['classroom'] = classroom
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateSubjectView(CreateView):
    template_name = 'teacher/create_subjects.html'
    form_class = SubjectCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        classroom = Classroom.objects.get(id=self.kwargs['pk'])
        self.object.classroom = classroom
        self.object.save()
        return redirect('teacher:subjects', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectDeleteView(DeleteView):
    model = Subject

    def get(self, *a, **kw):
        return self.delete(kw['pk'])

    def get_success_url(self):
        return reverse_lazy('teacher:subjects', kwargs={'pk': self.kwargs['cpk']})


@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['subject_name', 'image']
    template_name = 'teacher/subject_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cpk'] = self.kwargs['cpk']
        return context

    def get_success_url(self):
        return reverse_lazy('teacher:subjects', kwargs={'pk': self.kwargs['cpk']})


@method_decorator([login_required, teacher_required], name='dispatch')
class HomeTasksView(ListView):
    template_name = 'teacher/home_tasks.html'
    context_object_name = 'home_tasks'

    def get_queryset(self):
        subject = Subject.objects.get(id=self.kwargs['subj'])
        home_tasks = HomeTask.objects.filter(subject=subject).order_by('-pub_date')
        return home_tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        subject = Subject.objects.get(id=self.kwargs['subj'])
        context['subject'] = subject
        images = ImagesHT.objects.filter(home_task__subject=subject)
        context['images'] = images
        print(images)
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateHomeTaskView(CreateView):
    template_name = 'teacher/create_home_tasks.html'
    form_class = HomeworkCreateForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        subject = Subject.objects.get(id=self.kwargs['subj'])
        instance.subject = subject
        instance.save()

        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                ImagesHT.objects.create(image=image, home_task=instance)

        return redirect('teacher:home_tasks', pk=self.kwargs['pk'], subj=self.kwargs['subj'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        subject = Subject.objects.get(id=self.kwargs['subj'])
        context['subject'] = subject
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentWorksView(ListView):
    template_name = 'teacher/home_works.html'
    context_object_name = 'home_works'

    def get_queryset(self):
        home_works = StudentWork.objects.filter(student=self.kwargs['student_id']).order_by('-send_date')
        return home_works

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']

        context['st'] = Student.objects.get(user__id=self.kwargs['student_id'])
        return context
