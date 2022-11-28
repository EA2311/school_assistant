from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django import forms

from .models import User, Student, Teacher


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'patronymic')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'patronymic')


class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'patronymic')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user


class TeacherSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'patronymic')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        Teacher.objects.create(user=user)
        return user
