# Generated by Django 4.1.3 on 2022-12-11 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_studentwork_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentwork',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]