# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Estacion, Vehiculo, Conductor, Viaje, Turno, Dispositivo, EcoScore
import json


@login_required(login_url="/login/")
def index(request):
    return redirect('dashboard')  # Redirect to dashboard

@login_required(login_url="/login/")
def dashboard_view(request):
    context = {'segment': 'dashboard'}
    return render(request, 'home/dashboard.html', context)

@login_required(login_url="/login/")
def estaciones_view(request):
    estaciones = Estacion.objects.all()
    return render(request, 'home/estaciones.html', {'estaciones': estaciones})

@login_required(login_url="/login/")
def vehiculos_view(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'home/vehiculos.html', {'vehiculos': vehiculos})

@login_required(login_url="/login/")
def conductores_view(request):
    conductores = Conductor.objects.all()
    return render(request, 'home/conductores.html', {'conductores': conductores})


def get_vehicle_routes():
    # Obtener detalles de eco_scores
    eco_scores = EcoScore.objects.values('id', 'start_timestamp', 'end_timestamp', 'distancia_recorrida', 'eventos_reales', 'puntuacion_ecologica', 'harsh_accelerations', 'harsh_brakings', 'harsh_cornerings', 'geojson_data')
    for score in eco_scores:
        score['geojson_data'] = json.dumps(score['geojson_data'])
    return list(eco_scores)
@login_required(login_url="/login/")
def viajes_view(request):
    eco_scores = get_vehicle_routes()
    return render(request, 'home/viajes.html', {'routes': eco_scores})

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
