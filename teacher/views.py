from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required
from accounts.models import Teacher, Student
from student.models import StudentWork, ImagesSW
from teacher.forms import ClassroomCreateForm, SubjectCreateForm, HomeworkCreateForm
from teacher.models import Classroom, Subject, HomeTask, ImagesHT, Mark
from teacher.services import get_current_teacher_classrooms, get_current_teacher, \
    get_current_classroom_students_with_annotation, get_current_classroom


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

    def get(self, *a, **kwargs):
        return self.delete(*a, **kwargs)


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateClassroomsView(CreateView):
    template_name = 'teacher/create_classroom.html'
    form_class = ClassroomCreateForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.teacher = get_current_teacher(self.request.user)
        instance.save()
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
        return Subject.objects.filter(classroom__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['classroom'] = get_current_classroom(self.kwargs['pk'])
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
        """
        Return queryset of StudentWork objects which belong to current student and ordered by send date with related
        HomeTask, Subject, Student and User objects.
        """
        return StudentWork.objects.select_related('home_task__subject', 'student__user'). \
            filter(student=self.kwargs['student_id']).order_by('-send_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = Student.objects.select_related('user').get(user=self.kwargs['student_id'])

        images = ImagesHT.objects.select_related('home_task').filter(home_task__subject__classroom=self.kwargs['pk'])

        images_sw = ImagesSW.objects.select_related('work__home_task').filter(work__student__user=student.user.id)

        marks = Mark.objects.select_related('homework').filter(homework__student=student)

        context['pk'] = self.kwargs['pk']
        context['st'] = student
        context['images'] = images
        context['images_sw'] = images_sw
        context['marks'] = marks

        return context

    def post(self, request, *args, **kwargs):
        mark = request.POST.get('mark_')
        comment = request.POST.get('comment_')
        print(mark, comment)
        teacher = Teacher.objects.get(user=request.user)
        hw = StudentWork.objects.get(id=request.POST.get('submit'))

        Mark.objects.create(mark=mark, comment=comment, teacher=teacher, homework=hw)
        hw.is_checked = True
        hw.save()
        return redirect('teacher:homework', self.kwargs['pk'], hw.student.user.id)
