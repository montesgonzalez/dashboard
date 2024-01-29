# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Estacion(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=100)  # Ejemplo: Centro de trabajo, parking

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    matricula = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    año = models.IntegerField()
    estado = models.CharField(max_length=50)
    estacion = models.ForeignKey('Estacion', on_delete=models.CASCADE)
    dispositivo = models.OneToOneField('Dispositivo', on_delete=models.SET_NULL, null=True, related_name='vehiculo_asociado')

    def __str__(self):
        return self.matricula


class Conductor(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=50)
    licencia = models.CharField(max_length=50)
    contacto = models.CharField(max_length=100)
    estacion = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Turno(models.Model):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    # Más campos según necesidades

    def __str__(self):
        return f"{self.inicio} - {self.fin} | {self.conductor.nombre}"


class Dispositivo(models.Model):
    imei = models.CharField(max_length=50)
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, null=True, blank=True, related_name='dispositivo_asociado')

    def __str__(self):
        return self.imei


class Viajes(models.Model):
    imei = models.CharField(max_length=15, null=True, blank=True)  # Nuevo campo para IMEI
    start_timestamp = models.DateTimeField(blank=True, null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    distancia_recorrida = models.FloatField(blank=True, null=True)
    eventos_permitidos_por_km = models.FloatField(blank=True, null=True)
    eventos_reales = models.IntegerField(blank=True, null=True)
    puntuacion_ecologica = models.FloatField(blank=True, null=True)
    harsh_accelerations = models.IntegerField(blank=True, null=True)
    harsh_brakings = models.IntegerField(blank=True, null=True)
    harsh_cornerings = models.IntegerField(blank=True, null=True)
    geojson_data = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'viajes'


