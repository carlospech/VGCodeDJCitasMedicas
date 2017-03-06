from django import forms
from citasmedicas.models import Secretaria, Paciente


class LoginForm(forms.Form):
    usuario = forms.CharField()
    contrasena = forms.CharField(widget=forms.PasswordInput)


class SecretariaForm(forms.ModelForm):

    class Meta:
        model = Secretaria
        fields = ('nombre', 'telefono_personal')


class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ('doctor', 'nombre', 'apellido_paterno',
                  'apellido_materno', 'telefono_personal',
                  'fecha_nacimiento')