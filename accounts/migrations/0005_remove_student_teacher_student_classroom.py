# Generated by Django 4.1.3 on 2022-11-29 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_homework'),
        ('accounts', '0004_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='teacher.classroom'),
            preserve_default=False,
        ),
    ]
