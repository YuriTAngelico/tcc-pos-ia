from django.urls import path

from . import views

urlpatterns = [
    path('', views.Employee.as_view(), name='index'),
]