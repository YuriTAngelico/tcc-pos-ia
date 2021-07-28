from django.urls import path

from . import views

urlpatterns = [
    path('', views.Employee.as_view(), name='employee'),
    path('add-photo', views.Photo.as_view(), name='add-photo'),
]