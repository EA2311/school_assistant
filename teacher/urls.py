from django.urls import path

from teacher.views import ClassroomsView, CreateClassroomsView, DetailClassroomView, SubjectsView, CreateSubjectView

app_name = 'teacher'


urlpatterns = [
    path('', ClassroomsView.as_view(), name='classrooms'),
    path('new_classroom/', CreateClassroomsView.as_view(), name='create_classroom'),
    path('<int:pk>/', DetailClassroomView.as_view(), name='detail_classroom'),
    path('<int:pk>/subjects/', SubjectsView.as_view(), name='subjects'),
    path('<int:pk>/subjects/new/', CreateSubjectView.as_view(), name='create_subjects')

]
