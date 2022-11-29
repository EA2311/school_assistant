from django import forms

from teacher.models import Classroom, Subject, Homework


class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ('teacher', 'key',)


class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ('classroom', )


class HomeworkCreateForm(forms.ModelForm):
    class Meta:
        model = Homework
        exclude = ('subject', )

