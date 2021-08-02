from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
import os

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=30, default='first_name')
    last_name = models.CharField(max_length=30, default='last_name')
    age = models.IntegerField(default=0)
    job_position = models.CharField(max_length=30, default='*')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.first_name + self.last_name


class EmployeeFacePhoto(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='employee_photo/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.employee.first_name + self.employee.last_name


class EmployeeFaceVideo(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    video = models.FileField(upload_to='employee_video/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.employee.first_name + self.employee.last_name


class Bloob(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    bloob = models.JSONField(default=dict)
    mask = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.employee.first_name + self.employee.last_name


class AIModel(models.Model):
    name = models.CharField(max_length=30, default='my_model')
    model = models.FileField(upload_to='models/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class AIDetector(models.Model):
    name = models.CharField(max_length=30, default='face_detector')
    face_detection_model = models.FileField(upload_to='ai_face_detector/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class AIRecognizer(models.Model):
    name = models.CharField(max_length=30, default='recognizer')
    recognizer = models.FileField(upload_to='ai_recognizer/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class AILabel(models.Model):
    name = models.CharField(max_length=30, default='labels')
    labels = models.FileField(upload_to='ai_labels/')
    timestamp = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name