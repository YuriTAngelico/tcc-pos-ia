# Generated by Django 3.2.5 on 2021-08-08 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('face_recognition', '0003_auto_20210807_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aiembedder',
            name='caffee_model',
        ),
        migrations.RemoveField(
            model_name='historicalaiembedder',
            name='caffee_model',
        ),
    ]