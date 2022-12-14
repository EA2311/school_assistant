from django.urls import path, include

from accounts.views import StudentSignUpView, TeacherSignUpView, HomeView, login_request, SignUpView


app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name='home'),

    path('student/login/', login_request, name='student_login'),
    path('teacher/login/', login_request, name='teacher_login'),

    path('signup/', SignUpView.as_view(), name='home_signup'),

    path('student/signup/', StudentSignUpView.as_view(), name='student_signup'),
    path('teacher/signup/', TeacherSignUpView.as_view(), name='teacher_signup'),
]
