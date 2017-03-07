from django.contrib import admin
from citasmedicas.models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    fields = ('usuario', 'nombres', 'apellido_paterno', 'apellido_materno', 'titulo', 'especialidad', 'cedula_profesional', 'cedula_especialidad', 'registro_ssa')
    list_display = ('nombres', 'apellido_paterno', 'apellido_materno', 'titulo', 'especialidad')

admin.site.register(Doctor, DoctorAdmin)