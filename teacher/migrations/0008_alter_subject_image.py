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
            field=models.ImageField(default='https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png', upload_to=teacher.models.subject_file_name),
        ),
    ]
