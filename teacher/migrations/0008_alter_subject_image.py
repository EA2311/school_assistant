# Generated by Django 4.1.3 on 2022-12-08 14:12

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_subject_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='image',
            field=models.ImageField(default='placeholder_image.png', upload_to=teacher.services.models_services.generate_file_name),
        ),
    ]
