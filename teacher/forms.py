from django import forms

from teacher.models import Classroom, Subject


class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ('teacher', 'key',)


class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ('classroom', )

