from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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
        subject = Subject.objects.get(id=self.kwargs['subj'])
        home_tasks = HomeTask.objects.filter(subject=subject).order_by('-pub_date')
        return home_tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(id=self.kwargs['subj'])
        context['subject'] = subject
        student = Student.objects.get(user=self.request.user)
        context['student'] = student
        subjects = Subject.objects.filter(classroom=student.classroom)
        context["subjects"] = subjects
        try:
            hw = StudentWork.objects.filter(home_task__subject=subject, student__user=self.request.user)
            context['hws'] = hw
        except ObjectDoesNotExist:
            pass

        return context


@method_decorator([login_required, student_required], name='dispatch')
class StudentDetailHomeworkView(DetailView):
    model = HomeTask
    template_name = 'student/detail_home_tasks.html'
    context_object_name = 'home_task'

    def post(self, request, subj, pk):
        student = Student.objects.get(user=request.user)
        ht = HomeTask.objects.get(id=pk)
        sw = StudentWork.objects.create(home_task=ht, text=request.POST.get('hw_text'), student=student)

        images = self.request.FILES.getlist('hw_images')
        if images:
            for image in images:
                ImagesSW.objects.create(image=image, work=sw)

        return HttpResponseRedirect(reverse('student:detail_home_tasks', args=(subj, pk,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        context['student'] = student
        ht = self.kwargs['pk']
        try:
            hw = StudentWork.objects.get(home_task=ht, student__user=self.request.user)
            context['hw'] = hw
        except ObjectDoesNotExist:
            pass
        try:
            hw = StudentWork.objects.get(home_task=ht, student__user=self.request.user)
            mark = Mark.objects.get(homework=hw)
            context['mark'] = mark
        except ObjectDoesNotExist:
            pass
        try:
            images = ImagesHT.objects.filter(home_task=ht)
            context['images'] = images
        except ObjectDoesNotExist:
            pass
        try:
            images = ImagesSW.objects.filter(work=StudentWork.objects.get(home_task=ht, student__user=self.request.user))
            context['images_sw'] = images
        except ObjectDoesNotExist:
            pass

        return context
