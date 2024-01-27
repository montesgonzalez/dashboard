# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # La página de inicio
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Secciones específicas
    path('estaciones/', views.estaciones_view, name='estaciones'),
    path('vehiculos/', views.vehiculos_view, name='vehiculos'),
    path('conductores/', views.conductores_view, name='conductores'),
    path('viajes/', views.viajes_view, name='viajes'),
    path('turnos/', views.turnos_view, name='turnos'),
    path('dispositivos/', views.dispositivos_view, name='dispositivos'),

    # Coincide con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),
]


