from django.contrib import admin
from citasmedicas.models import Doctor, Paciente

class DoctorAdmin(admin.ModelAdmin):
    fields = ('usuario', 'nombres', 'apellido_paterno', 'apellido_materno', 'titulo', 'especialidad', 'cedula_profesional', 'cedula_especialidad', 'registro_ssa')
    list_display = ('nombres', 'apellido_paterno', 'apellido_materno', 'titulo', 'especialidad')

class PacienteAdmin(admin.ModelAdmin):
    list_filter = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Paciente, PacienteAdmin)
