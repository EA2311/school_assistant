from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required

from teacher.forms import ClassroomCreateForm, SubjectCreateForm, HomeTaskCreateForm
from teacher.models import Classroom, Subject, HomeTask, ImagesHT
from teacher.services import (
    get_current_teacher_classrooms,
    create_classroom,
    get_current_classroom_students_with_annotation,
    get_current_subject,
    get_student_work_with_related_objects,
    get_current_student_with_user,
    get_home_task_images_with_task,
    get_student_work_images_with_task,
    get_current_student_marks,
    create_mark_for_student_work,
    get_student_work_with_user,
    get_classroom_subjects,
    create_subject,
    create_home_task,
)


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassroomsView(ListView):
    template_name = 'teacher/classrooms.html'
    context_object_name = 'classrooms'

    def get_queryset(self):
        """Gets a queryset of classrooms related to current teacher."""
        return get_current_teacher_classrooms(self.request.user)


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassroomDeleteView(DeleteView):
    success_url = reverse_lazy('teacher:classrooms')
    model = Classroom

    def get(self, *a, **kwargs):  # TODO: is get method a right way to delete object in this scope?
        return self.delete(*a, **kwargs)


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateClassroomsView(CreateView):
    template_name = 'teacher/create_classroom.html'
    form_class = ClassroomCreateForm

    def form_valid(self, form):
        create_classroom(form, self.request.user)
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
        context['pk'] = self.kwargs['pk']
        context['students'] = get_current_classroom_students_with_annotation(self.object)
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectsView(ListView):
    template_name = 'teacher/subjects.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return get_classroom_subjects(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateSubjectView(CreateView):
    template_name = 'teacher/create_subjects.html'
    form_class = SubjectCreateForm

    def form_valid(self, form):
        pk = self.kwargs['pk']
        create_subject(form, pk)
        return redirect('teacher:subjects', pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectDeleteView(DeleteView):
    model = Subject

    def get(self, *a, **kw):  # TODO: is get method a right way to delete object in this scope?
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
        """
        Return queryset of HomeTask objects which belong to current subject and ordered by publishing date.
        """
        return HomeTask.objects.filter(subject__id=self.kwargs['subj']).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get current Subject object
        subject = Subject.objects.get(id=self.kwargs['subj'])

        context['pk'] = self.kwargs['pk']
        context['subject'] = subject

        # Get queryset of ImagesHT objects which belong to current subject and related HomeTask objects
        context['images'] = ImagesHT.objects.select_related('home_task').filter(home_task__subject=subject)
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateHomeTaskView(CreateView):
    template_name = 'teacher/create_home_tasks.html'
    form_class = HomeTaskCreateForm

    def form_valid(self, form):
        subject_id = self.kwargs['subj']
        create_home_task(form, subject_id, self.request.FILES.getlist('images'))
        return redirect('teacher:home_tasks', pk=self.kwargs['pk'], subj=subject_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['subject'] = get_current_subject(self.kwargs['subj'])
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class HomeTaskDeleteView(DeleteView):
    model = HomeTask

    def get(self, *a, **kwargs):
        return self.delete(kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('teacher:home_tasks', kwargs={'pk': self.kwargs['cpk'], 'subj': self.kwargs['subj']})


@method_decorator([login_required, teacher_required], name='dispatch')
class HomeTaskUpdateView(UpdateView):
    model = HomeTask
    fields = ['task']
    template_name = 'teacher/home_task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cpk'] = self.kwargs['cpk']
        context['subj'] = self.kwargs['subj']
        return context

    def get_success_url(self):
        return reverse_lazy('teacher:home_tasks', kwargs={'pk': self.kwargs['cpk'], 'subj': self.kwargs['subj']})


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentWorksView(ListView):
    template_name = 'teacher/home_works.html'
    context_object_name = 'home_works'

    def get_queryset(self):
        return get_student_work_with_related_objects(self.kwargs['student_id'])

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        student = get_current_student_with_user(self.kwargs['student_id'])

        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        context['st'] = student
        context['images'] = get_home_task_images_with_task(pk)
        context['images_sw'] = get_student_work_images_with_task(student.user.id)
        context['marks'] = get_current_student_marks(student)
        return context

    def post(self, request, *args, **kwargs):
        student_work = get_student_work_with_user(request.POST.get('submit'))
        create_mark_for_student_work(request.POST.get('mark_'), request.POST.get('comment_'), request.user, student_work)
        return redirect('teacher:homework', self.kwargs['pk'], student_work.student.user.id)
