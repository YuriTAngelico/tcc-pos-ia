from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *
# Register your models here.

class EmployeeHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['first_name', 'last_name', 'age', 'job_position', 'timestamp',]
    history_list_display = ['first_name', 'last_name', 'age', 'job_position', 'timestamp',]
    list_filter = ['age', 'job_position',]
admin.site.register(Employee, EmployeeHistoryAdmin)


class PhotoHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'timestamp',]
    history_list_display = ['employee', 'timestamp',]
    list_filter = ['employee', 'timestamp',]
admin.site.register(Photo, PhotoHistoryAdmin)


class BloobHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'mask', 'timestamp',]
    history_list_display = ['employee', 'mask', 'timestamp',]
    list_filter = ['employee', 'mask', 'timestamp',]
admin.site.register(Bloob, BloobHistoryAdmin)


class AIDetectorHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(AIDetector, AIDetectorHistoryAdmin)


class AIRecognizerHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(AIRecognizer, AIRecognizerHistoryAdmin)


class AILabelHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(AILabel, AILabelHistoryAdmin)