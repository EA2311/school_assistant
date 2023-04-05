# Generated by Django 4.1.3 on 2022-12-10 18:51

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0009_alter_subject_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='image',
            field=models.ImageField(default='placeholder_image.png', upload_to=teacher.models.subject_file_name),
        ),
    ]
