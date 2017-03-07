from django import forms
from django.contrib.auth.models import User
from citasmedicas.models import Secretaria


class LoginForm(forms.Form):
    usuario = forms.CharField()
    contrasena = forms.CharField(widget=forms.PasswordInput)


class SecretariaForm(forms.ModelForm):
    usuario = forms.CharField()
    contrasena = forms.CharField(widget=forms.PasswordInput)
    repite_contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Secretaria
        fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'telefono_personal')


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