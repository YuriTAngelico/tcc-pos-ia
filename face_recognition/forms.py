from django import forms
from .models import *

#####################################
# cria os forms para os models do MPA
#####################################

class EmployeeForm(forms.ModelForm):
    first_name=forms.CharField(initial="yuri",label='First name',widget=forms.TextInput(attrs={'placeholder': 'Enter first name', 'id':'first_name'}),max_length=50,required=True)
    last_name=forms.CharField(initial="angelico",label='Last name',widget=forms.TextInput(attrs={'placeholder': 'Enter last name', 'id':'last_name'}),max_length=50,required=True)
    age=forms.IntegerField(initial="25",label='Age',required=True)
    job_position=forms.CharField(initial="engineer",label='Job position',widget=forms.TextInput(attrs={'placeholder': 'Enter job position', 'id':'job_position'}),max_length=50,required=True)
    video=forms.FileField(label='Upload the video of the employee',required=True, widget=forms.FileInput(attrs={'accept':'video/*'}))
    class Meta:
        model = Employee
        fields=['first_name','last_name','age','job_position','video']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = EmployeeFacePhoto
        fields=['employee', 'photo']


class TestImageForm(forms.ModelForm):
    class Meta:
        model = TestImage
        fields="__all__"