from django.urls import path

from . import views

urlpatterns = [
    path('', views.EmployeeClass.as_view(), name='employee'),
    path('employees-registered', views.EmployeeClass.employees_registered, name='employees_registered'),
    path('employee/delete/<int:id>', views.EmployeeClass.delete, name='employee-delete'),
    # path('add-photo', views.Photo.as_view(), name='add-photo'),
    path('tests', views.Test.as_view(), name='test_recognition'),
    path('tests/receive-post', views.Test.ajax_post, name='tests-receive-post'),
    path('faq', views.AboutProjectClass.as_view(), name='about_the_project'),
]