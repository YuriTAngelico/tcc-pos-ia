from django.urls import path

from . import views

urlpatterns = [
    path('', views.EmployeeClass.as_view(), name='employee'),
    path('employee/delete/<int:id>', views.EmployeeClass.delete, name='employee-delete'),
    path('add-photo', views.Photo.as_view(), name='add-photo'),
    path('tests', views.Test.as_view(), name='tests'),
]