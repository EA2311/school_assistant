from rest_framework import serializers
from accounts.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Teacher
        fields = ['user', 'user.first_name', 'user.last_name', 'user.patronymic', 'user.phone_number']
