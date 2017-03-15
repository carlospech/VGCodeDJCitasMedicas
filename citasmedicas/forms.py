# coding: utf-8
from django import forms
from citasmedicas.models import Secretaria, Paciente, Consultorio, Doctor
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget


class LoginForm(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Contraseña'}))


class SecretariaForm(forms.ModelForm):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Contraseña'}))
    repite_contrasena = forms.CharField(label='Repite contraseña',
                                        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Contraseña'}))

    class Meta:
        model = Secretaria
        fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'telefono_personal')
        labels = {
            'telefono_personal': 'Teléfono personal'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno'}),
            'telefono_personal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono personal',
                                                          'max': '9999999999'})
        }

    def clean_usuario(self):
        datos_limpios = self.cleaned_data
        usuario = datos_limpios.get('usuario')
        if User.objects.filter(username=usuario).exists():
            raise forms.ValidationError("El usuario '%s' ya existe. Capture uno nuevo." % usuario)
        return usuario

    def clean_repite_contrasena(self):
        datos_limpios = self.cleaned_data
        contrasena = datos_limpios.get('contrasena')
        repite_contrasena = datos_limpios.get('repite_contrasena')
        if contrasena != repite_contrasena:
            raise forms.ValidationError("La contraseña no es igual, intente de nuevo.")
        return repite_contrasena


class SecretariaEditForm(forms.ModelForm):

    class Meta:
        model = Secretaria
        fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'telefono_personal')
        labels = {
            'telefono_personal': 'Teléfono personal'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno'}),
            'telefono_personal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono personal',
                                                          'max': '9999999999'})
        }


class PacienteForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    apellido_paterno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'apellido_paterno'}))
    apellido_materno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'apellido_materno'}))
    telefono_personal = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'telefono_personal'}))
    fecha_nacimiento = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Paciente
        fields = ('nombre', 'apellido_paterno',
                  'apellido_materno', 'telefono_personal',
                  'fecha_nacimiento')


class ConsultorioForm(forms.ModelForm):

    class Meta:
        model = Consultorio
        fields = ('doctor', 'descripcion', 'direccion')
