from django import forms
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
        fields = ('nombre', 'telefono_personal')