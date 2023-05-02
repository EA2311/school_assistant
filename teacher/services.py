from typing import Optional

from django.db.models import QuerySet, Count, Q

from accounts.models import Teacher, User, Student
from teacher.models import Classroom, Subject, ImagesHT, HomeTask


def get_current_teacher(user: User) -> Teacher:
    """Returns current teacher object."""
    return Teacher.objects.get(user=user)


def get_current_teacher_classrooms(user: User) -> QuerySet[Classroom]:
    """Returns current teacher`s classrooms queryset."""
    return Classroom.objects.filter(teacher=get_current_teacher(user))


def _get_current_classroom_students(classroom: Classroom) -> QuerySet[Student]:
    """Returns a queryset of students who are in the current classroom."""
    return Student.objects.select_related('user').filter(classroom=classroom).order_by('user__last_name')


def _count_unchecked_student_homeworks() -> Count:
    """Returns a Count aggregator for unchecked student's homeworks."""
    return Count('studentwork', filter=Q(studentwork__is_checked=False))


def get_current_classroom_students_with_annotation(classroom: Classroom) -> QuerySet[Student]:
    """
    Returns a queryset of students who are in the current classroom with annotated whether homework has been checked.
    """
    return _get_current_classroom_students(classroom).annotate(unchecked=_count_unchecked_student_homeworks())


def get_current_classroom(classroom_id: int) -> Classroom:
    """Returns a Classroom object of a current classroom by id."""
    return Classroom.objects.get(id=classroom_id)


def get_current_subject(subject_id: int) -> Subject:
    """Returns a Subject object of a current subject by id."""
    return Subject.objects.get(id=subject_id)


def save_home_task_images(images: Optional[list], task: HomeTask) -> None:
    """If home task images have been uploaded, creates and objects of ImagesHT for each of them."""
    if images:
        for image in images:
            ImagesHT.objects.create(image=image, home_task=task)
