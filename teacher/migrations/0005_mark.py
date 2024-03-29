# Generated by Django 4.1.3 on 2022-12-02 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_studentwork_student'),
        ('accounts', '0008_alter_student_classroom'),
        ('teacher', '0004_homework'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('send_date', models.DateTimeField(auto_now_add=True)),
                ('homework', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.studentwork')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
        ),
    ]
