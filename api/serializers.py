from rest_framework import serializers
from accounts.models import Teacher, User


class UserSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'phone_number')


class TeacherSerializer(serializers.ModelSerializer):
    """

    """
    user = UserSerializer(required=True)

    class Meta:
        model = Teacher
        fields = ['user']
