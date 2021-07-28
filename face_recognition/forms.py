from django import forms
from .models import *

#####################################
# cria os forms para os models do MPA
#####################################

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields="__all__"


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields="__all__"


class BloobForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields="__all__"