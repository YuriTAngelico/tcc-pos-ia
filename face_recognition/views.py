from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .forms import *

class Employee(View):

    def get(self, request):

        data = {}
        data['employee_form'] = EmployeeForm()
        return render(request, 'index.html', data)


    def post(self, request):
        pass