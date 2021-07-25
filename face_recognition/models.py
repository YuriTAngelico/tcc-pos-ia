from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
import os

def models_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'models')
def ia_files_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'ia_files')

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=30, default='first_name')
    last_name = models.CharField(max_length=30, default='last_name')
    age = models.IntegerField(max_length=3, default=0)
    job_position = models.CharField(max_length=30, default='*')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.first_name

class Photos(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    bloob = models.JSONField(default=dict)
    mask = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.employee.first_name

class IAModel(models.Model):
    model = models.FileField(upload_to='models')
    model_path = models.FilePathField(path=models_path, recursive=True)

class IAFiles(models.Model):
    face_detection_model = models.FilePathField(path=ia_files_path, recursive=True)
    recognizer = models.FilePathField(path=ia_files_path, recursive=True)
    labels = models.FilePathField(path=ia_files_path, recursive=True)
