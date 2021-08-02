from django import forms
from .models import *

#####################################
# cria os forms para os models do MPA
#####################################

class EmployeeForm(forms.ModelForm):
    first_name=forms.CharField(initial="",label='First name',widget=forms.TextInput(attrs={'placeholder': 'Enter first name', 'id':'first_name'}),max_length=50,required=True)
    last_name=forms.CharField(initial="",label='Last name',widget=forms.TextInput(attrs={'placeholder': 'Enter last name', 'id':'last_name'}),max_length=50,required=True)
    age=forms.IntegerField(initial="",label='Age',required=True)
    job_position=forms.CharField(initial="",label='Job position',widget=forms.TextInput(attrs={'placeholder': 'Enter job position', 'id':'job_position'}),max_length=50,required=True)
    class Meta:
        model = Employee
        fields=['first_name','last_name','age','job_position']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = EmployeePhoto
        fields=['employee', 'photo']


class BloobForm(forms.ModelForm):
    class Meta:
        model = Bloob
        fields="__all__"