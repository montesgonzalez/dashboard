# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
import os
import ssl
import time

from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import EstacionForm, VehiculoForm
from .models import Dispositivo
from .models import Estacion, Conductor, Turno, Viajes
from .models import Vehiculo
import redis

# views.py

import json
import redis
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Dispositivo

from django.shortcuts import render, get_object_or_404
from .models import Dispositivo
from pusher import Pusher

from django.shortcuts import render, get_object_or_404
from .models import Dispositivo
from django.conf import settings
from pusher import Pusher
from django.views.decorators.csrf import csrf_exempt
# settings.py
REDIS_HOST = 'us1-climbing-cowbird-40081.upstash.io'
REDIS_PORT = 40081
REDIS_PASSWORD = '1212460ce61a4ef6b549248b4fd9d9a0'
REDIS_SSL = True


### SEND COMMANDS TO REDIS

@csrf_exempt
def send_command(request, imei):
    if request.method == 'POST':
        data = json.loads(request.body)
        command = data.get('command')

        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            ssl=REDIS_SSL,
            ssl_cert_reqs=None  # Desactivar la verificación del certificado SSL
        )

        try:
            command_data = {'imei': imei, 'command': command}
            r.publish('comandos', json.dumps(command_data))
            return JsonResponse({'status': 'success', 'message': f'Comando enviado a {imei}'})
        except redis.exceptions.ConnectionError as e:
            return JsonResponse({'status': 'error', 'message': f'Error al conectar con Redis: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


# Inicializar Pusher
pusher_client = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

def lista_dispositivos_view(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, 'lista_dispositivos.html', {'dispositivos': dispositivos})

def tracking_view(request, imei):
    dispositivo = get_object_or_404(Dispositivo, imei=imei)
    pusher_channel = f'dispositivo-{imei}'

    return render(request, 'dispositivo_detalle.html', {
        'dispositivo': dispositivo,
        'pusher_key': settings.PUSHER_KEY,
        'pusher_channel': pusher_channel
    })




def get_redis_connection():
    return redis.Redis(
        host='us1-climbing-cowbird-40081.upstash.io',
        port=40081,
        password='1212460ce61a4ef6b549248b4fd9d9a0',
        ssl=True,
        ssl_cert_reqs=None  # Desactivar la verificación del certificado SSL
    )


# views.py

# views.py

from .models import Dispositivo


def dispositivos_view(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, 'lista_dispositivos.html', {'dispositivos': dispositivos})


def dispositivo_sse_view(request):
    imei = request.GET.get('imei')
    if not imei:
        return render(request, 'dispositivo_sse_form.html')

    get_object_or_404(Dispositivo, imei=imei)

    # Resto del código de la función permanece igual

    def event_stream():
        r = get_redis_connection()
        pubsub = r.pubsub()
        pubsub.subscribe(f'ubicaciones:{imei}')  # Suscribirse a un canal específico basado en el IMEI

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                yield f"data: {json.dumps(data)}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


def detalle_dispositivo(request, imei):
    # Renderizar la plantilla con el contexto del IMEI
    return render(request, 'dispositivo_sse.html', {'imei': imei})


def dispositivos_view(request):
    dispositivos = Dispositivo.objects.all()
    print("Dispositivos recuperados:", dispositivos)  # Impresión para depuración
    return render(request, 'dispositivos.html', {'dispositivos': dispositivos})


from django.shortcuts import render, get_object_or_404
from .models import Dispositivo


def mqtt_view(request):
    return render(request, 'mqtt.html')


@login_required(login_url="/login/")
def index(request):
    return redirect('dashboard')  # Redirect to dashboard


@login_required(login_url="/login/")
def dashboard_view(request):
    context = {'segment': 'dashboard'}
    return render(request, 'home/dashboard.html', context)


# Estaciones
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


# Vehiculos
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
    eco_scores = Viajes.objects.values('id', 'start_timestamp', 'end_timestamp', 'distancia_recorrida',
                                       'eventos_reales', 'puntuacion_ecologica', 'harsh_accelerations',
                                       'harsh_brakings', 'harsh_cornerings', 'geojson_data')
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
