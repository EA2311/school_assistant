from django.test import TestCase

from accounts.models import Teacher, User
from teacher.models import Classroom, Subject, HomeTask, ImagesHT


class ImageHT:
    pass


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
        cls.home_task = HomeTask.objects.create(task='task', subject=cls.subject)
        cls.imageHT = ImagesHT.objects.create(image='filename.png', home_task=cls.home_task)


class ClassroomModelTest(TeacherTestCase):
    def test_classroom_object_name_is_class_name_field(self):
        classroom = self.classroom
        expected_object_name = classroom.class_name
        self.assertEqual(expected_object_name, str(classroom))


class SubjectModelTest(TeacherTestCase):
    def test_subject_object_name_is_subject_name_field(self):
        subject = self.subject
        expected_object_name = subject.subject_name
        self.assertEqual(expected_object_name, str(subject))


class HomeTaskModelTest(TeacherTestCase):
    def test_hometask_object_name_is_task_field_with_pub_date(self):
        home_task = self.home_task
        expected_object_name = f'{home_task.task} - {home_task.pub_date}'
        self.assertEqual(expected_object_name, str(home_task))


class ImagesHTModelTest(TeacherTestCase):
    def test_imageht_object_name_is_image_field_with_home_task_field(self):
        imageHT = self.imageHT
        expected_object_name = f'{imageHT.image} - {imageHT.home_task}'
        self.assertEqual(expected_object_name, str(imageHT))


