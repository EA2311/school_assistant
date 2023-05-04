from django import forms

from teacher.models import Classroom, Subject, HomeTask


class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ('teacher', 'key',)


class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ('classroom', )


class HomeTaskCreateForm(forms.ModelForm):
    class Meta:
        model = HomeTask
        exclude = ('subject', )

