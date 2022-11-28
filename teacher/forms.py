from django import forms
from django.db import transaction

from teacher.models import Classroom


class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ('teacher', 'key',)



