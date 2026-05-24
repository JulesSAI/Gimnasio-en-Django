from django.db import models

class Sede(models.Model):
    id_sede = models.AutoField(primary_key=True)
    nombre_sede = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    capacidad_maxima_personas = models.IntegerField(null=True, blank=True)
    coordenadas_gps = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'sede'

    def __str__(self):
        return self.nombre_sede

class CatalogoEjercicios(models.Model):
    id_ejercicio = models.AutoField(primary_key=True)
    nombre_ejercicio = models.CharField(max_length=150)
    grupo_muscular_principal = models.CharField(max_length=100, null=True, blank=True)
    tipo_ejercicio = models.CharField(max_length=50, null=True, blank=True)
    url_video_tutorial = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'catalogo_ejercicios'

    def __str__(self):
        return self.nombre_ejercicio

class Series(models.Model):
    id_serie = models.AutoField(primary_key=True)
    cantidad_series = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'series'

    def __str__(self):
        return str(self.cantidad_series)

class Repeticiones(models.Model):
    id_repeticion = models.AutoField(primary_key=True)
    cantidad_repeticiones = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'repeticiones'

    def __str__(self):
        return str(self.cantidad_repeticiones)

class Descanso(models.Model):
    id_descanso = models.AutoField(primary_key=True)
    tiempo_segundos = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'descanso'

    def __str__(self):
        return str(self.tiempo_segundos)

class Entrenador(models.Model):
    id_entrenador = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    anios_experiencia = models.IntegerField(null=True, blank=True)
    id_sede_base = models.ForeignKey(Sede, models.DO_NOTHING, db_column='id_sede_base')

    class Meta:
        managed = False
        db_table = 'entrenador'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    estado_suscripcion = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    id_sede_principal = models.ForeignKey(Sede, models.DO_NOTHING, db_column='id_sede_principal', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Maquina(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    nombre_maquina = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, null=True, blank=True)
    estado_mantenimiento = models.CharField(max_length=50, blank=True, null=True)
    id_sede = models.ForeignKey(Sede, models.DO_NOTHING, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'maquina'

    def __str__(self):
        return self.nombre_maquina

class PerfilMedico(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(Usuario, models.DO_NOTHING, db_column='id_usuario')
    grupo_sanguineo = models.CharField(max_length=5, null=True, blank=True)
    alergias = models.TextField(null=True, blank=True)
    lesiones_previas = models.TextField(null=True, blank=True)
    peso_actual_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentaje_grasa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    objetivo_fisico = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'perfil_medico'

class ClaseGrupal(models.Model):
    id_clase = models.AutoField(primary_key=True)
    nombre_clase = models.CharField(max_length=100)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    capacidad_maxima = models.IntegerField()
    id_sede = models.ForeignKey(Sede, models.DO_NOTHING, db_column='id_sede')
    id_entrenador = models.ForeignKey(Entrenador, models.DO_NOTHING, db_column='id_entrenador')

    class Meta:
        managed = False
        db_table = 'clase_grupal'

    def __str__(self):
        return self.nombre_clase

class Rutina(models.Model):
    id_rutina = models.AutoField(primary_key=True)
    nivel_dificultad = models.CharField(max_length=50, null=True, blank=True)
    estado_rutina = models.CharField(max_length=50, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_entrenador = models.ForeignKey(Entrenador, models.DO_NOTHING, db_column='id_entrenador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rutina'

    def __str__(self):
        return f"Rutina {self.id_rutina} - {self.id_usuario.nombres}"

class ReservaClase(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    fecha_hora_reserva = models.DateTimeField(blank=True, null=True)
    estado_reserva = models.CharField(max_length=50, blank=True, null=True)
    id_clase = models.ForeignKey(ClaseGrupal, models.DO_NOTHING, db_column='id_clase')
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'reserva_clase'

class SesionEntrenamiento(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    fecha_hora_registro = models.DateTimeField(blank=True, null=True)
    duracion_minutos = models.IntegerField(null=True, blank=True)
    metricas_registradas = models.TextField(null=True, blank=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_sede = models.ForeignKey(Sede, models.DO_NOTHING, db_column='id_sede')
    id_rutina = models.ForeignKey(Rutina, models.DO_NOTHING, db_column='id_rutina', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sesion_entrenamiento'

class RutinaEjercicio(models.Model):
    id_rutina_ejercicio = models.AutoField(primary_key=True)
    id_rutina = models.ForeignKey(Rutina, models.DO_NOTHING, db_column='id_rutina')
    id_ejercicio = models.ForeignKey(CatalogoEjercicios, models.DO_NOTHING, db_column='id_ejercicio')
    id_serie = models.ForeignKey(Series, models.DO_NOTHING, db_column='id_serie')
    id_repeticion = models.ForeignKey(Repeticiones, models.DO_NOTHING, db_column='id_repeticion')
    id_descanso = models.ForeignKey(Descanso, models.DO_NOTHING, db_column='id_descanso')

    class Meta:
        managed = False
        db_table = 'rutina_ejercicio'
