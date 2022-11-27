from django.urls import path

from teacher.views import ClassroomsView

app_name = 'teacher'

urlpatterns = [
    path('', ClassroomsView.as_view(), name='classrooms'),
]
