from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *
# Register your models here.

class EmployeeHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['first_name', 'last_name', 'age', 'job_position', 'video', 'timestamp',]
    history_list_display = ['first_name', 'last_name', 'age', 'job_position', 'video', 'timestamp',]
    list_filter = ['age', 'job_position',]
admin.site.register(Employee, EmployeeHistoryAdmin)


class EmployeePhotoHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'timestamp',]
    history_list_display = ['employee', 'timestamp',]
    list_filter = ['employee', 'timestamp',]
admin.site.register(EmployeeFacePhoto, EmployeePhotoHistoryAdmin)


class BloobHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['employee', 'mask', 'timestamp',]
    history_list_display = ['employee', 'mask', 'timestamp',]
    list_filter = ['employee', 'mask', 'timestamp',]
admin.site.register(Bloob, BloobHistoryAdmin)


class AIEmbedderHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(AIEmbedder, AIEmbedderHistoryAdmin)

class AIFaceDetectorHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'caffee_model', 'timestamp',]
    history_list_display = ['name', 'caffee_model', 'timestamp',]
    list_filter = ['name', 'caffee_model', 'timestamp',]
admin.site.register(AIFaceDetector, AIFaceDetectorHistoryAdmin)


class EmbeddingsHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(Embedding, EmbeddingsHistoryAdmin)


class RecognizerHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(Recognizer, RecognizerHistoryAdmin)


class LabelHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'timestamp',]
    history_list_display = ['name', 'timestamp',]
    list_filter = ['name', 'timestamp',]
admin.site.register(Label, RecognizerHistoryAdmin)