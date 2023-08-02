import random
import string


def get_random_string():
    """Return a unique string of a random sequence of lower and uppercase characters and digits 40 characters long."""
    symbols = string.ascii_letters + string.digits
    return ''.join(random.choice(symbols) for _ in range(40))


def generate_file_name(instance, filename):
    """Returns a full filename string for uploaded image depending on an instance class."""
    ext = filename.split('.')[-1]
    from teacher.models import Classroom, Subject, ImagesHT

    if isinstance(instance, Classroom):
        filename = f'teacher_{instance.teacher.user.id}/{instance.class_name}/cover.{ext}'
    elif isinstance(instance, Subject):
        filename = f'teacher_{instance.classroom.teacher.user.id}/{instance.classroom.class_name}/' \
                   f'{instance.subject_name}/cover.{ext}'
    elif isinstance(instance, ImagesHT):
        filename = f'teacher_{instance.home_task.subject.classroom.teacher.user.id}/' \
                   f'{instance.home_task.subject.classroom}/{instance.home_task.subject.subject_name}/home_tasks/' \
                   f'{instance.home_task.pub_date}.{ext}'
    return filename
