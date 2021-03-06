from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=30, default='first_name')
    last_name = models.CharField(max_length=30, default='last_name')
    age = models.IntegerField(default=0)
    job_position = models.CharField(max_length=30, default='*')
    video = models.FileField(upload_to='employee_video/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.first_name + self.last_name


class EmployeeFacePhoto(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employee_photo/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.employee.first_name + self.employee.last_name


class EmployeeEmbedding(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    embedding_data = models.JSONField(default=dict)
    mask = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.employee.first_name + self.employee.last_name


class AIEmbedder(models.Model):
    name = models.CharField(max_length=30, default='embedder')
    embedder = models.FileField(upload_to='ai_embedder/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class AIFaceDetector(models.Model):
    name = models.CharField(max_length=30, default='face_detector')
    face_detection_model = models.FileField(upload_to='ai_face_detector/')
    caffee_model = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class TestImage(models.Model):
    name = models.CharField(max_length=30, default='test_image')
    test_image = models.FileField(upload_to='test_images/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name