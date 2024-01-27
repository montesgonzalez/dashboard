# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EcoScores(models.Model):
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
        managed = False
        db_table = 'eco_scores'


class HomeConductor(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=50)
    licencia = models.CharField(max_length=50)
    contacto = models.CharField(max_length=100)
    estacion = models.ForeignKey('HomeEstacion', models.DO_NOTHING, blank=True, null=True)
    vehiculo = models.ForeignKey('HomeVehiculo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_conductor'


class HomeDispositivo(models.Model):
    imei = models.CharField(max_length=50)
    vehiculo = models.OneToOneField('HomeVehiculo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_dispositivo'


class HomeEstacion(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'home_estacion'


class HomeTurno(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    conductor = models.ForeignKey(HomeConductor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'home_turno'


class HomeVehiculo(models.Model):
    matricula = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    año = models.IntegerField()
    estado = models.CharField(max_length=50)
    dispositivo = models.OneToOneField(HomeDispositivo, models.DO_NOTHING, blank=True, null=True)
    estacion = models.ForeignKey(HomeEstacion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'home_vehiculo'


class HomeViaje(models.Model):
    ruta = models.TextField()
    duracion = models.DurationField()
    conductor = models.ForeignKey(HomeConductor, models.DO_NOTHING)
    vehiculo = models.ForeignKey(HomeVehiculo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'home_viaje'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class VehicleTrackingData350612077921425(models.Model):
    field_timestamp_field = models.DateTimeField(db_column='_timestamp_', blank=True, null=True)  # Field renamed because it started with '_'. Field renamed because it ended with '_'.
    server_time = models.DateTimeField(blank=True, null=True)
    ignition = models.IntegerField(blank=True, null=True)
    eco_score = models.FloatField(blank=True, null=True)
    trip_odometer = models.FloatField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)  # This field type is a guess.
    green_driving_value = models.FloatField(blank=True, null=True)
    green_driving_type = models.IntegerField(blank=True, null=True)
    green_driving_event_duration = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    total_odometer = models.FloatField(blank=True, null=True)
    digital_input_1 = models.IntegerField(blank=True, null=True)
    trip_status = models.IntegerField(blank=True, null=True)
    eventid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_tracking_data_350612077921425'


class VehicleTrackingData357073294119942(models.Model):
    field_timestamp_field = models.DateTimeField(db_column='_timestamp_', blank=True, null=True)  # Field renamed because it started with '_'. Field renamed because it ended with '_'.
    server_time = models.DateTimeField(blank=True, null=True)
    ignition = models.IntegerField(blank=True, null=True)
    eco_score = models.FloatField(blank=True, null=True)
    trip_odometer = models.FloatField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)  # This field type is a guess.
    green_driving_value = models.FloatField(blank=True, null=True)
    green_driving_type = models.IntegerField(blank=True, null=True)
    green_driving_event_duration = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    total_odometer = models.FloatField(blank=True, null=True)
    digital_input_1 = models.IntegerField(blank=True, null=True)
    trip_status = models.IntegerField(blank=True, null=True)
    eventid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_tracking_data_357073294119942'
