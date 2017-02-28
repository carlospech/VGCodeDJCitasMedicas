from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Doctor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    titulo = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=50, blank=True, null=True)
    cedula_profesional = models.CharField(max_length=8)
    cedula_especialidad = models.CharField(max_length=8)
    registro_ssa = models.CharField(max_length=8)

    class Meta(object):
        verbose_name_plural = 'Doctores'

    def __str__(self):
        return self.nombre


class Secretaria(models.Model):
    doctor = models.ForeignKey(Doctor)
    nombre = models.CharField(max_length=150)
    telefono_personal = models.IntegerField()

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    doctor = models.ForeignKey(Doctor)
    nombre = models.CharField(max_length=150)
    telefono_personal = models.IntegerField()
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.nombre


class Consultorio(models.Model):
    doctor = models.ForeignKey(Doctor)
    descripcion = models.CharField(max_length=50)
    direccion = models.TextField()

    def __str__(self):
        return self.descripcion


class Horario(models.Model):
    consultorio = models.ForeignKey(Consultorio)
    DIA_DOMINGO = 'DO'
    DIA_LUNES = 'LU'
    DIA_MARTES = 'MA'
    DIA_MIERCOLES = 'MI'
    DIA_JUEVES = 'JU'
    DIA_VIERNES = 'VI'
    DIA_SABADO = 'SA'
    DIA_SEMANA_CHOICES = (
        (DIA_DOMINGO, 'Domingo'),
        (DIA_LUNES, 'Lunes'),
        (DIA_MARTES, 'Martes'),
        (DIA_MIERCOLES, 'Miercoles'),
        (DIA_JUEVES, 'Jueves'),
        (DIA_VIERNES, 'Viernes'),
        (DIA_SABADO, 'Sabado'),
    )
    dia_semana = models.CharField(
        max_length=2,
        choices=DIA_SEMANA_CHOICES,
        default=DIA_LUNES,
    )
    hora_inicio = models.TimeField()
    hara_fin = models.TimeField()

    def __str__(self):
        return self.dia_semana


class Cita(models.Model):
    consultorio = models.ForeignKey(Consultorio)
    paciente = models.ForeignKey(Paciente)
    fecha = models.DateField()
    hora = models.TimeField()


class Receta(models.Model):
    consultorio = models.ForeignKey(Consultorio)
    paciente = models.ForeignKey(Paciente)
    fecha = models.DateField()
    hora = models.TimeField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    talla = models.CharField(max_length=20)
    peso = models.CharField(max_length=20)
    edad = models.CharField(max_length=20)
