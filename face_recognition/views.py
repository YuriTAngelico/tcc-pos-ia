from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from .forms import *

class Employee(View):

    def get(self, request):

        data = {}
        data['employee_form'] = EmployeeForm()
        data['photo_form'] = PhotoForm()

        return render(request, 'employee.html', data)

    def post(self, request):

        print("[INFO] Adding employee.")

        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Employee {request.POST['first_name']} {request.POST['last_name']} succesfully created!", extra_tags="employee")
            return redirect('employee')

        else:
            messages.error(request, "Error on creating, invalid form!", extra_tags="employee")
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
            messages.error(request, f"Error on adding, invalid form! - {e}", extra_tags="employee")
            return redirect('employee')