from django.urls import path

from teacher.views import ClassroomsView

app_name = 'accounts'

urlpatterns = [
    path('', ClassroomsView.as_view(), name='home'),
]