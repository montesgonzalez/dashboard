from django import forms
from .models import Estacion, Vehiculo


class EstacionForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ['nombre', 'ubicacion', 'capacidad', 'tipo']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['matricula', 'modelo', 'marca', 'año', 'estado', 'estacion', 'dispositivo']

