# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from .models import Estacion, Vehiculo, Conductor, Viaje, Turno, Dispositivo
# Registro de modelos en el admin de Django
admin.site.register(Estacion)
admin.site.register(Vehiculo)
admin.site.register(Conductor)
admin.site.register(Viaje)
admin.site.register(Turno)
admin.site.register(Dispositivo)
