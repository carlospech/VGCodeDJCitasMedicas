from django.contrib import admin
from citasmedicas.models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    fields = ('usuario', 'nombre', 'titulo', 'especialidad', 'cedula_profesional', 'cedula_especialidad', 'registro_ssa')
    list_display = ('nombre', 'titulo', 'especialidad')

admin.site.register(Doctor, DoctorAdmin)