from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

#custom imports
import cv2

#app imports
from .forms import *
from .models import *

class Employee(View):

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

        photos = EmployeeFacePhoto.objects.all()

        for photo in photos:
            cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE)
            img = cv2.imread(str(photo.photo))
            imS = cv2.resize(img, (600, 600))
            cv2.imshow("output", imS)
            cv2.waitKey(0) # waits until a key is pressed
            cv2.destroyAllWindows() # destroys the window showing image

        return HttpResponse("Teste...")