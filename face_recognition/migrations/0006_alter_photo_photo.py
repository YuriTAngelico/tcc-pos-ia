# Generated by Django 3.2.5 on 2021-07-25 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_recognition', '0005_auto_20210725_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.FileField(upload_to='employee_photo/'),
        ),
    ]