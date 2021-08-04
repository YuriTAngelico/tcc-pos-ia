from django.core.files.base import File
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image
from django.core.files.base import ContentFile

#custom imports
import cv2
import os
import matplotlib.pyplot as plt

#app imports
from .forms import *
from .models import *

class EmployeeClass(View):

    def get(self, request):

        data = {}
        data['employee_form'] = EmployeeForm()
        data['photo_form'] = PhotoForm()

        return render(request, 'employee.html', data)

    def post(self, request):

        print("[INFO] Adding employee.")

        form = EmployeeForm(request.POST, request.FILES)

        print(request.POST)

        try:
            form.save()
            messages.success(request, f"Employee {request.POST['first_name']} {request.POST['last_name']} succesfully created!", extra_tags="employee")
            return redirect('employee')

        except Exception as e:
            messages.error(request, f"Error on creating, invalid form! --> {e}", extra_tags="employee")
            form = EmployeeForm()
            return redirect('employee')



class Photo(View):

    def post(self, request):

        print("[INFO] Adding employee photo.")

        print(request.POST)
        print(request.FILES)

        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"Photo succesfully added!", extra_tags="employee")
            return redirect('employee')

        else:
            messages.error(request, f"Error on adding, invalid form!", extra_tags="employee")
            return redirect('employee')

class Test(View):

    def get(self, request):

        detectors = AIDetector.objects.all()

        for detector in detectors:
            print(detector.face_detection_model)

            with open(str(detector.face_detection_model), 'r') as file:
                pass

        employees = Employee.objects.all()

        for employee in employees:
            print(employee.video)

            source  = cv2.VideoCapture(str(employee.video))
            success,image = source.read()
            count = 0
            # while success:
            while count < 2:

                success,image = source.read()
                print('Read a new frame: ', success)
                path = os.path.dirname(os.path.realpath(__file__)) + f"\\photo_temp\\{employee.first_name}{employee.last_name}-photo{count}.jpg"
                cv2.imwrite(path, image)

                with open(os.path.dirname(os.path.realpath(__file__)) + f"\\photo_temp\\{employee.first_name}{employee.last_name}-photo{count}.jpg", 'rb') as f:
                    data = f.read()

                new_face_photo = EmployeeFacePhoto()
                new_face_photo.employee = Employee.objects.get(id=employee.id)
                new_face_photo.photo.save(f"{employee.first_name}{employee.last_name}-photo{count}.jpg", ContentFile(data))
                new_face_photo.save()

                face = EmployeeFacePhoto.objects.all().last()

                count += 1

        return HttpResponse("Teste...")