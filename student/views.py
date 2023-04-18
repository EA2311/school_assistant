from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist

from accounts.decorators import student_required
from accounts.models import Student
from teacher.models import Classroom, Subject, HomeTask, Mark, ImagesHT
from student.models import StudentWork, ImagesSW


@method_decorator([login_required, student_required], name='dispatch')
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
        classroom = Classroom.objects.get(key=request.POST.get("key"))
        student.classroom = classroom
        student.save()
        return redirect('student:student_classrooms')


@method_decorator([login_required, student_required], name='dispatch')
class StudentHomeworksView(ListView):
    template_name = 'student/student_homeworks.html'
    context_object_name = 'home_tasks'

    def get_queryset(self):
        """
        Return queryset of HomeTask objects which belong to current subject and ordered by publishing date with related
        HomeTask, Subject, Student and User objects.
        """
        return get_list_or_404(
            HomeTask.objects.select_related('subject').order_by('-pub_date'),subject=self.kwargs['subj']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subject = Subject.objects.get(id=self.kwargs['subj'])
        student = Student.objects.get(user=self.request.user)
        subjects = Subject.objects.filter(classroom=student.classroom)

        # If student's work for this subject exists, get queryset of StudentWork with related HomeTask and Mark objects
        try:
            hw = StudentWork.objects.select_related('home_task', 'mark').filter(
                home_task__subject=subject, student__user=self.request.user)
        except ObjectDoesNotExist:
            pass
        else:
            context['hws'] = hw

        context['subject'] = subject
        context['student'] = student
        context["subjects"] = subjects
        return context


@method_decorator([login_required, student_required], name='dispatch')
class StudentDetailHomeworkView(DetailView):
    model = HomeTask
    template_name = 'student/detail_home_tasks.html'
    context_object_name = 'home_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = Student.objects.get(user=self.request.user)

        home_task_id = self.kwargs['pk']

        student_work = StudentWork.objects.get_or_none(home_task=home_task_id, student__user=self.request.user)
        mark = Mark.objects.get_or_none(homework=student_work)
        images_ht = ImagesHT.objects.filter_or_none(home_task=home_task_id)
        images_sw = ImagesSW.objects.filter_or_none(work=student_work)

        context['student'] = student
        context['hw'] = student_work
        context['mark'] = mark
        context['images'] = images_ht
        context['images_sw'] = images_sw

        return context

    def post(self, request, subj, pk):
        student = Student.objects.get(user=request.user)
        ht = HomeTask.objects.get(id=pk)
        sw = StudentWork.objects.create(home_task=ht, text=request.POST.get('hw_text'), student=student)

        images = self.request.FILES.getlist('hw_images')
        if images:
            for image in images:
                ImagesSW.objects.create(image=image, work=sw)

        return HttpResponseRedirect(reverse('student:detail_home_tasks', args=(subj, pk,)))
