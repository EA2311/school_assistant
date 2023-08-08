from django.test import TestCase

from accounts.models import Teacher, User
from teacher.models import Classroom, Subject


class TeacherTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(email='test@gmail.com',
                                   phone_number='12412414214',
                                   first_name='Fname',
                                   last_name='Lname',
                                   patronymic='Pname',
                                   is_teacher=True
                                   )

        cls.teacher = Teacher.objects.create(user=cls.user)

        cls.classroom = Classroom.objects.create(class_name='1-A',
                                                 key='asdsfssafsffadvfaefsca',
                                                 image='img.png',
                                                 teacher=cls.teacher
                                                 )
        cls.subject = Subject.objects.create(subject_name='Math', classroom=cls.classroom, image='1.png')


class ClassroomModelTest(TeacherTestCase):

    def test_classroom_object_name_is_class_name_field(self):
        classroom = self.classroom
        expected_object_name = classroom.class_name
        self.assertEqual(expected_object_name, str(classroom))


class SubjectModelTest(TeacherTestCase):

    def test_subject_object_name_is_class_name_field(self):
        subject = self.subject
        expected_object_name = subject.subject_name
        self.assertEqual(expected_object_name, str(subject))
