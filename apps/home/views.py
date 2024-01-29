# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import EstacionForm, VehiculoForm
from .models import Estacion, Vehiculo, Conductor, Turno, Dispositivo,Viajes
import json


@login_required(login_url="/login/")
def index(request):
    return redirect('dashboard')  # Redirect to dashboard

@login_required(login_url="/login/")
def dashboard_view(request):
    context = {'segment': 'dashboard'}
    return render(request, 'home/dashboard.html', context)

#Estaciones
@login_required(login_url="/login/")
def estaciones_view(request):
    estaciones = Estacion.objects.all()
    return render(request, 'home/estaciones.html', {'estaciones': estaciones})

@login_required(login_url="/login/")
def crear_estacion(request):
    if request.method == 'POST':
        form = EstacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estaciones_view')
    else:
        form = EstacionForm()
    return render(request, 'home/crear_estacion.html', {'form': form})

@login_required(login_url="/login/")
def editar_estacion(request, estacion_id):
    estacion = get_object_or_404(Estacion, pk=estacion_id)
    if request.method == 'POST':
        form = EstacionForm(request.POST, instance=estacion)
        if form.is_valid():
            form.save()
            return redirect('estaciones_view')
    else:
        form = EstacionForm(instance=estacion)
    return render(request, 'home/editar_estacion.html', {'form': form, 'estacion': estacion})
@login_required(login_url="/login/")
def vehiculos_view(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'home/vehiculos.html', {'vehiculos': vehiculos})

#Vehiculos
@login_required(login_url="/login/")
def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehiculos_view')
    else:
        form = VehiculoForm()
    return render(request, 'home/crear_vehiculo.html', {'form': form})

@login_required(login_url="/login/")
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('vehiculos_view')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'home/editar_vehiculo.html', {'form': form, 'vehiculo': vehiculo})

@login_required(login_url="/login/")
def conductores_view(request):
    conductores = Conductor.objects.all()
    return render(request, 'home/conductores.html', {'conductores': conductores})


def get_vehicle_routes():
    # Obtener detalles de eco_scores
    eco_scores = Viajes.objects.values('id', 'start_timestamp', 'end_timestamp', 'distancia_recorrida', 'eventos_reales', 'puntuacion_ecologica', 'harsh_accelerations', 'harsh_brakings', 'harsh_cornerings', 'geojson_data')
    for score in eco_scores:
        score['geojson_data'] = json.dumps(score['geojson_data'])
    return list(eco_scores)


@login_required(login_url="/login/")
def viajes_view(request):
    viajes = Viajes.objects.all()

    viajes_data = []
    for viaje in viajes:
        dispositivo = Dispositivo.objects.filter(imei=viaje.imei).first() if viaje.imei else None
        vehiculo = dispositivo.vehiculo if dispositivo else None
        conductor = Conductor.objects.filter(vehiculo=vehiculo).first() if vehiculo else None

        viaje_data = {
            'id': viaje.id,
            'conductor_nombre': conductor.nombre if conductor else 'Conductor no asignado',
            'vehiculo': vehiculo.matricula if vehiculo else 'Vehículo no asignado',
            'dispositivo': dispositivo.imei if dispositivo else 'Dispositivo no asignado',
            'estacion': vehiculo.estacion.nombre if vehiculo and vehiculo.estacion else 'Estación no asignada',
            'start_timestamp': viaje.start_timestamp,
            'end_timestamp': viaje.end_timestamp,
            'distancia_recorrida': viaje.distancia_recorrida,
            'eventos_reales': viaje.eventos_reales,
            'puntuacion_ecologica': viaje.puntuacion_ecologica,
        }
        viajes_data.append(viaje_data)

    return render(request, 'home/lista_viajes.html', {'viajes': viajes_data})
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url="/login/")
def lista_viajes_view(request):
    viajes = Viajes.objects.all()

    viajes_data = []
    for viaje in viajes:
        dispositivo = Dispositivo.objects.filter(imei=viaje.imei).first() if viaje.imei else None
        vehiculo = dispositivo.vehiculo if dispositivo else None
        conductor = Conductor.objects.filter(vehiculo=vehiculo).first() if vehiculo else None

        viaje_data = {
            'id': viaje.id,
            'conductor_nombre': conductor.nombre if conductor else 'Conductor no asignado',
            'vehiculo': vehiculo.matricula if vehiculo else 'Vehículo no asignado',
            'dispositivo': dispositivo.imei if dispositivo else 'Dispositivo no asignado',
            'estacion': vehiculo.estacion.nombre if vehiculo and vehiculo.estacion else 'Estación no asignada',
            'start_timestamp': viaje.start_timestamp,
            'end_timestamp': viaje.end_timestamp,
            'distancia_recorrida': viaje.distancia_recorrida,
            'eventos_reales': viaje.eventos_reales,
            'puntuacion_ecologica': viaje.puntuacion_ecologica,
        }
        viajes_data.append(viaje_data)

    return render(request, 'home/lista_viajes.html', {'viajes': viajes_data})
@login_required(login_url="/login/")
def viaje_detalle_view(request, viaje_id):
    viaje = Viajes.objects.get(id=viaje_id)
    dispositivo = Dispositivo.objects.filter(imei=viaje.imei).first() if viaje.imei else None
    vehiculo = dispositivo.vehiculo if dispositivo else None

    try:
        conductor = Conductor.objects.get(vehiculo=vehiculo)
        conductor_nombre = conductor.nombre
    except Conductor.DoesNotExist:
        conductor_nombre = 'Conductor no asignado'

    viaje_data = {
        'id': viaje.id,
        'conductor_nombre': conductor_nombre,
        'vehiculo': vehiculo.matricula if vehiculo else 'Vehículo no asignado',
        'dispositivo': dispositivo.imei if dispositivo else 'Dispositivo no asignado',
        'imei': viaje.imei,
        'start_timestamp': viaje.start_timestamp,
        'end_timestamp': viaje.end_timestamp,
        'distancia_recorrida': viaje.distancia_recorrida,
        'eventos_reales': viaje.eventos_reales,
        'puntuacion_ecologica': viaje.puntuacion_ecologica,
        'harsh_accelerations': viaje.harsh_accelerations,
        'harsh_brakings': viaje.harsh_brakings,
        'harsh_cornerings': viaje.harsh_cornerings,
        'geojson_data': json.dumps(viaje.geojson_data)
    }

    return render(request, 'home/detalle_viaje.html', {'viaje': viaje_data})
@login_required(login_url="/login/")
def turnos_view(request):
    turnos = Turno.objects.all()
    return render(request, 'home/turnos.html', {'turnos': turnos})

@login_required(login_url="/login/")
def dispositivos_view(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, 'home/dispositivos.html', {'dispositivos': dispositivos})

@login_required(login_url="/login/")
def pages(request):
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        context = {'segment': load_template}
        return render(request, f'home/{load_template}.html', context)

    except template.TemplateDoesNotExist:
        return render(request, 'home/page-404.html')

    except:
        return render(request, 'home/page-500.html')

# Puedes añadir más vistas según tus necesidades específicas
