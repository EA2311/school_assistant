from typing import Optional

from django.db.models import QuerySet, Count, Q

from accounts.models import Teacher, User, Student
from student.models import StudentWork, ImagesSW
from teacher.forms import ClassroomCreateForm
from teacher.models import Classroom, Subject, ImagesHT, HomeTask, Mark


def get_current_teacher(user: User) -> Teacher:
    """Returns current teacher object."""
    return Teacher.objects.get(user=user)


def create_classroom(form: ClassroomCreateForm, teacher: User) -> None:
    """Creates Classroom object, fill teacher field and save it in the database."""
    classroom = form.save(commit=False)
    classroom.teacher = get_current_teacher(teacher)
    classroom.save()


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


def get_student_work_with_related_objects(student_id: int) -> QuerySet[StudentWork]:
    """
    Returns a queryset of StudentWork objects which belong to current student and ordered by send date with related
    HomeTask, Subject, Student and User objects.
    """
    return StudentWork.objects.select_related('home_task__subject', 'student__user').filter(
        student=student_id).order_by('-send_date')


def get_current_student_with_user(user_id: int) -> Student:
    """Returns current Student object by user id with related User object."""
    return Student.objects.select_related('user').get(user=user_id)


def get_home_task_images_with_task(classroom_id: int) -> QuerySet[ImagesHT]:
    """Returns a ImagesHT queryset by classroom id with related HomeTask objects."""
    return ImagesHT.objects.select_related('home_task').filter(home_task__subject__classroom=classroom_id)


def get_student_work_images_with_task(user_id: int) -> QuerySet[ImagesSW]:
    """Returns a ImagesSW queryset by user id with related HomeTask objects."""
    return ImagesSW.objects.select_related('work__home_task').filter(work__student__user=user_id)


def get_current_student_marks(student: Student) -> QuerySet[Mark]:
    """Returns a Mark queryset by Student with related HomeTask objects."""
    return Mark.objects.select_related('homework').filter(homework__student=student)


def get_student_work_with_user(student_work_id: int) -> StudentWork:
    """Returns a StudentWork queryset by student work id with related User object."""
    return StudentWork.objects.select_related('student__user').get(id=student_work_id)


def create_mark_for_student_work(mark: str, comment: str, teacher_user: User, student_work: StudentWork) -> None:
    """Create a Mark object for current student work and mark StudentWork object as checked."""
    teacher = get_current_teacher(teacher_user)
    Mark.objects.create(mark=mark, comment=comment, teacher=teacher, homework=student_work)
    _mark_student_work_as_checked(student_work)


def _mark_student_work_as_checked(student_work: StudentWork) -> None:
    """Set is_checked field in StudentWork object as True and save it."""
    student_work.is_checked = True
    student_work.save()
