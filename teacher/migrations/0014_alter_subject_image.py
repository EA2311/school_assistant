# Generated by Django 4.1.3 on 2023-04-05 14:48

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0013_imagesht'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='image',
            field=models.ImageField(default='placeholder_image.webp', upload_to=teacher.services.models_services.generate_file_name),
        ),
    ]
