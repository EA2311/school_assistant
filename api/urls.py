from django.urls import path
from api.views import TeacherList, TeacherDetail

urlpatterns = [
    path('teachers/', TeacherList.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),
]