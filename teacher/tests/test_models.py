from django.test import TestCase

from accounts.models import Teacher, User
from teacher.models import Classroom


class ClassroomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create(email='test@gmail.com',
                                   phone_number='12412414214',
                                   first_name='Fname',
                                   last_name='Lname',
                                   patronymic='Pname',
                                   is_teacher=True
                                   )

        teacher = Teacher.objects.create(user=user)

        cls.classroom = Classroom.objects.create(class_name='1-A',
                                                 key='asdsfssafsffadvfaefsca',
                                                 image='img.png',
                                                 teacher=teacher
                                                 )

    def test_classroom_object_name_is_class_name_field(self):
        classroom = ClassroomModelTest.classroom
        expected_object_name = classroom.class_name
        self.assertEqual(expected_object_name, str(classroom))
