from typing import Optional

from accounts.models import User
from student.models import StudentWork
from teacher.forms import ClassroomCreateForm, SubjectCreateForm, HomeTaskCreateForm
from teacher.models import HomeTask, ImagesHT, Mark
from teacher.services.db_select import get_current_teacher, get_current_classroom, get_current_subject


def create_classroom(form: ClassroomCreateForm, teacher: User) -> None:
    """Creates a Classroom object, fill teacher field and save it in the database."""
    classroom = form.save(commit=False)
    classroom.teacher = get_current_teacher(teacher)
    classroom.save()


def create_subject(form: SubjectCreateForm, classroom_id: int) -> None:
    """Creates a new Subject object in the current Classroom."""
    subject = form.save(commit=False)
    subject.classroom = get_current_classroom(classroom_id)
    subject.save()


def create_home_task(form: HomeTaskCreateForm, subject_id: int, images: Optional[list]) -> None:
    """Creates a new HomeTask object for the current Subject and save images if they exist."""
    home_task = form.save(commit=False)
    home_task.subject = get_current_subject(subject_id)
    home_task.save()

    _save_home_task_images(images, home_task)


def _save_home_task_images(images: Optional[list], task: HomeTask) -> None:
    """If home task images have been uploaded, creates and objects of ImagesHT for each of them."""
    if images:
        for image in images:
            ImagesHT.objects.create(image=image, home_task=task)


def create_mark_for_student_work(mark: str, comment: str, teacher_user: User, student_work: StudentWork) -> None:
    """Create a Mark object for current student work and mark StudentWork object as checked."""
    teacher = get_current_teacher(teacher_user)
    Mark.objects.create(mark=mark, comment=comment, teacher=teacher, homework=student_work)
    _mark_student_work_as_checked(student_work)


def _mark_student_work_as_checked(student_work: StudentWork) -> None:
    """Set is_checked field in StudentWork object as True and save it."""
    student_work.is_checked = True
    student_work.save()
