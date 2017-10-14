from rest_framework import serializers
from citasmedicas.models import Doctor
from .models import User


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Doctor
        fields = ('id', 'usuario', 'nombres', 'apellido_paterno',
                  'apellido_materno',
                  'titulo', 'especialidad', 'cedula_profesional',
                  'cedula_especialidad', 'registro_ssa')
