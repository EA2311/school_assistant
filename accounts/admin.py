from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Student, Teacher


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'phone_number', 'first_name', 'last_name', 'patronymic')
    list_filter = ('email', 'is_staff', 'is_active', 'phone_number', 'first_name', 'last_name', 'patronymic')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Info', {'fields': ('first_name', 'last_name', 'patronymic', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_student', 'is_teacher')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'first_name', 'last_name', 'patronymic', 'phone_number')}
         ),
    )
    search_fields = ('email', 'phone_number', 'first_name', 'last_name', 'patronymic')
    ordering = ('email', 'phone_number', 'first_name', 'last_name', 'patronymic')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)