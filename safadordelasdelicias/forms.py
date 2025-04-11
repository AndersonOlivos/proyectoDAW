from django import forms
from .models import *

class FormularioEmpleado(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = '__all__'