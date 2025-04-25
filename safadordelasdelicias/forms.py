from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *

class FormularioEmpleado(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ['nombre', 'apellido', 'edad', 'sexo','dni','telefono','correo','direccion','password','puesto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'id':'inp-contrasenia','class': 'form-control'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo")