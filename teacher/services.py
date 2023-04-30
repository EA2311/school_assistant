from django.db.models import QuerySet

from accounts.models import Teacher, User
from teacher.models import Classroom


def get_current_teacher(user: User) -> Teacher:
    """Returns current teacher object"""
    return Teacher.objects.get(user=user)


def get_current_teacher_classrooms(user: User) -> QuerySet[Classroom]:
    """Returns current teacher`s classrooms queryset"""
    return Classroom.objects.filter(teacher=get_current_teacher(user))
