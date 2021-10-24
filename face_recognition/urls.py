from django.urls import path

from . import views

urlpatterns = [
    path('', views.EmployeeClass.as_view(), name='employee'),
    path('employee/delete/<int:id>', views.EmployeeClass.delete, name='employee-delete'),
    path('add-photo', views.Photo.as_view(), name='add-photo'),
    path('tests', views.Test.as_view(), name='tests'),
    path('tests/receive-post', views.Test.ajax_post, name='tests-receive-post'),
    path('tests/recongnize-test', views.Test.recognize_test, name='recognize-test')
]