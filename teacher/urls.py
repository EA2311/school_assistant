from django.urls import path

from teacher.views import ClassroomsView, CreateClassroomsView, DetailClassroomView, SubjectsView, CreateSubjectView, \
    HomeTasksView, CreateHomeTaskView, StudentWorksView, ClassroomDeleteView, ClassroomUpdateView, SubjectUpdateView, \
    SubjectDeleteView, HomeTaskDeleteView

app_name = 'teacher'


urlpatterns = [
    path('', ClassroomsView.as_view(), name='classrooms'),
    path('new_classroom/', CreateClassroomsView.as_view(), name='create_classroom'),
    path('classroom/<int:pk>/', DetailClassroomView.as_view(), name='detail_classroom'),
    path('classroom/<int:pk>/delete/', ClassroomDeleteView.as_view(), name='delete_classroom'),
    path('classroom/<int:pk>/update/', ClassroomUpdateView.as_view(), name='update_classroom'),

    path('classroom/<int:pk>/homework/<int:student_id>/', StudentWorksView.as_view(), name='homework'),

    path('classroom/<int:pk>/subjects/', SubjectsView.as_view(), name='subjects'),
    path('classroom/<int:pk>/subjects/new/', CreateSubjectView.as_view(), name='create_subjects'),
    path('classroom/<int:cpk>/subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='delete_subject'),
    path('classroom/<int:cpk>/subjects/<int:pk>/update/', SubjectUpdateView.as_view(), name='update_subject'),

    path('classroom/<int:pk>/subjects/<int:subj>/home_tasks/', HomeTasksView.as_view(), name='home_tasks'),
    path('classroom/<int:pk>/subjects/<int:subj>/home_tasks/new/', CreateHomeTaskView.as_view(), name='create_home_tasks'),
    path('classroom/<int:cpk>/subjects/<int:subj>/home_tasks/<int:pk>/delete/', HomeTaskDeleteView.as_view(), name='delete_home_task'),

]
