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
class Viaje(models.Model):
    ruta = models.TextField()
    duracion = models.DurationField()
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    # Campos adicionales para puntuaciones ecológicas y comportamiento de conducción

    def __str__(self):
        return f"{self.vehiculo.matricula} - {self.conductor.nombre}"

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

class EcoScore(models.Model):
    id = models.AutoField(primary_key=True)
    device_imei = models.CharField(max_length=15)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    distancia_recorrida = models.FloatField()
    eventos_permitidos_por_km = models.FloatField()
    eventos_reales = models.IntegerField()
    puntuacion_ecologica = models.FloatField()
    harsh_accelerations = models.IntegerField()
    harsh_brakings = models.IntegerField()
    harsh_cornerings = models.IntegerField()
    geojson_data = models.JSONField()
    viaje = models.ForeignKey('Viaje', on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Viaje

    class Meta:
        db_table = 'eco_scores'


