import random
import string


def get_random_string():
    """Return a unique string of a random sequence of lower and uppercase characters and digits 40 characters long."""
    symbols = string.ascii_letters + string.digits
    return ''.join(random.choice(symbols) for _ in range(40))


def classroom_file_name(instance, filename):
    """Returns a full filename string for created Classroom image."""
    ext = filename.split('.')[-1]
    filename = f"teacher_{instance.teacher.user.id}/{instance.class_name}.{ext}"
    return filename


def subject_file_name(instance, filename):
    """Returns a full filename string for created Subject image."""
    ext = filename.split('.')[-1]
    filename = f"teacher_{instance.classroom.class_name}/{instance.subject_name}.{ext}"
    return filename


def ht_file_name(instance, filename):
    """Returns a full filename string for created HomeTask image."""
    ext = filename.split('.')[-1]
    filename = f'teacher_{instance.home_task.subject.classroom.teacher.user.id}/' + \
               f'{instance.home_task.subject.subject_name}/{instance.home_task.pub_date}.{ext}'
    return filename

