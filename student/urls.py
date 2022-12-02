from django.urls import path

from student.views import StudentClassroomView, StudentHomeworksView, StudentDetailHomeworkView

app_name = 'student'


urlpatterns = [
    path('', StudentClassroomView.as_view(), name='student_classrooms'),
    path('<int:subj>/', StudentHomeworksView.as_view(), name='home_works'),

    path('<int:subj>/homework/<int:pk>/', StudentDetailHomeworkView.as_view(), name='detail_home_tasks'),
    # path('<int:subj>/homework/<int:pk>/submit/', send, name='send'),


]
