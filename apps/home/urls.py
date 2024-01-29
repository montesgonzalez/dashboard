# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import viajes_view, viaje_detalle_view
urlpatterns = [
    # La página de inicio
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Secciones específicas
    #Estaciones
    path('estaciones/', views.estaciones_view, name='estaciones_view'),
    path('estaciones/crear/', views.crear_estacion, name='crear_estacion'),
    path('estaciones/editar/<int:estacion_id>/', views.editar_estacion, name='editar_estacion'),
    #Vehiculos
    path('vehiculos/', views.vehiculos_view, name='vehiculos_view'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', views.editar_vehiculo, name='editar_vehiculo'),
    #Conductores
    path('conductores/', views.conductores_view, name='conductores'),

    #Viajes
    path('viajes/', viajes_view, name='lista_viajes'),
    path('viajes/<int:viaje_id>/', viaje_detalle_view, name='detalle_viaje'),

    path('turnos/', views.turnos_view, name='turnos'),
    path('dispositivos/', views.dispositivos_view, name='dispositivos'),

    # Coincide con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),
]


