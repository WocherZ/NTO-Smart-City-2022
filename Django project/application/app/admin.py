from django.contrib import admin
from .models import Room, Patient, Doctor, Analysis


# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    pass


class PatientAdmin(admin.ModelAdmin):
    pass


class DoctorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Room, RoomAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Analysis)
