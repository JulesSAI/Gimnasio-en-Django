from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, IntegrityError
from django.contrib import messages
from .models import (
    Sede, CatalogoEjercicios, Series, Repeticiones, Descanso, Entrenador, 
    Usuario, Maquina, PerfilMedico, ClaseGrupal, Rutina, ReservaClase, 
    SesionEntrenamiento, RutinaEjercicio
)
from .forms import (
    SedeForm, CatalogoEjerciciosForm, SeriesForm, RepeticionesForm, DescansoForm, 
    EntrenadorForm, UsuarioForm, MaquinaForm, PerfilMedicoForm, ClaseGrupalForm, 
    RutinaForm, ReservaClaseForm, SesionEntrenamientoForm, RutinaEjercicioForm
)

def format_records(records):
    formatted = []
    for record in records:
        fields = []
        for f in record._meta.fields:
            val = getattr(record, f.name)
            if hasattr(val, '__str__') and f.is_relation:
                val_str = str(val) if val is not None else "-"
            else:
                val_str = str(val) if val is not None else "-"
            fields.append({'name': f.name, 'value': val_str})
        formatted.append({'pk': record.pk, 'fields': fields})
    return formatted

def home(request):
    models_list = [
        ('Sede', 'crud_sede'),
        ('Catalogo Ejercicios', 'crud_catalogo_ejercicios'),
        ('Series', 'crud_series'),
        ('Repeticiones', 'crud_repeticiones'),
        ('Descanso', 'crud_descanso'),
        ('Entrenador', 'crud_entrenador'),
        ('Usuario', 'crud_usuario'),
        ('Maquina', 'crud_maquina'),
        ('Perfil Medico', 'crud_perfil_medico'),
        ('Clase Grupal', 'crud_clase_grupal'),
        ('Rutina', 'crud_rutina'),
        ('Reserva Clase', 'crud_reserva_clase'),
        ('Sesion Entrenamiento', 'crud_sesion_entrenamiento'),
        ('Rutina Ejercicio', 'crud_rutina_ejercicio'),
    ]
    return render(request, 'gym/home.html', {'models_list': models_list})

# Original Views
def listar_usuarios(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id_usuario, u.nombres, u.apellidos, u.email, u.estado_suscripcion,
                   s.nombre_sede
            FROM USUARIO u
            LEFT JOIN SEDE s ON u.id_sede_principal = s.id_sede;
        """)
        usuarios = cursor.fetchall()
    return render(request, 'gym/usuarios.html', {'usuarios': usuarios})

def clases_por_sede(request, sede_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.nombre_clase, c.fecha_hora_inicio, c.fecha_hora_fin,
                   e.nombres || ' ' || e.apellidos as entrenador
            FROM CLASE_GRUPAL c
            JOIN ENTRENADOR e ON c.id_entrenador = e.id_entrenador
            WHERE c.id_sede = %s
            ORDER BY c.fecha_hora_inicio;
        """, [sede_id])
        clases = cursor.fetchall()
    return render(request, 'gym/clases.html', {'clases': clases, 'sede_id': sede_id})

def listar_sedes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_sede, nombre_sede, ciudad, capacidad_maxima_personas
            FROM SEDE
            ORDER BY ciudad;
        """)
        sedes = cursor.fetchall()
    return render(request, 'gym/sedes.html', {'sedes': sedes})

# --- CRUD Views ---

# 1. Sede
def crud_sede(request):
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sede agregada exitosamente.")
            return redirect('crud_sede')
    else:
        form = SedeForm()
    records = format_records(Sede.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Sede', 'delete_url_name': 'delete_sede'})

def delete_sede(request, pk):
    record = get_object_or_404(Sede, pk=pk)
    try:
        record.delete()
        messages.success(request, "Sede eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la Sede porque hay otros registros que dependen de ella.")
    return redirect('crud_sede')

# 2. CatalogoEjercicios
def crud_catalogo_ejercicios(request):
    if request.method == 'POST':
        form = CatalogoEjerciciosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ejercicio agregado exitosamente.")
            return redirect('crud_catalogo_ejercicios')
    else:
        form = CatalogoEjerciciosForm()
    records = format_records(CatalogoEjercicios.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Catalogo de Ejercicios', 'delete_url_name': 'delete_catalogo_ejercicios'})

def delete_catalogo_ejercicios(request, pk):
    record = get_object_or_404(CatalogoEjercicios, pk=pk)
    try:
        record.delete()
        messages.success(request, "Ejercicio eliminado correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar este ejercicio porque hay rutinas u otros registros que dependen de él.")
    return redirect('crud_catalogo_ejercicios')

# 3. Series
def crud_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Serie agregada exitosamente.")
            return redirect('crud_series')
    else:
        form = SeriesForm()
    records = format_records(Series.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Series', 'delete_url_name': 'delete_series'})

def delete_series(request, pk):
    record = get_object_or_404(Series, pk=pk)
    try:
        record.delete()
        messages.success(request, "Serie eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la serie porque otros registros dependen de ella.")
    return redirect('crud_series')

# 4. Repeticiones
def crud_repeticiones(request):
    if request.method == 'POST':
        form = RepeticionesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Repeticiones agregadas exitosamente.")
            return redirect('crud_repeticiones')
    else:
        form = RepeticionesForm()
    records = format_records(Repeticiones.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Repeticiones', 'delete_url_name': 'delete_repeticiones'})

def delete_repeticiones(request, pk):
    record = get_object_or_404(Repeticiones, pk=pk)
    try:
        record.delete()
        messages.success(request, "Repeticiones eliminadas correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar porque otros registros dependen de esto.")
    return redirect('crud_repeticiones')

# 5. Descanso
def crud_descanso(request):
    if request.method == 'POST':
        form = DescansoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Descanso agregado exitosamente.")
            return redirect('crud_descanso')
    else:
        form = DescansoForm()
    records = format_records(Descanso.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Descanso', 'delete_url_name': 'delete_descanso'})

def delete_descanso(request, pk):
    record = get_object_or_404(Descanso, pk=pk)
    try:
        record.delete()
        messages.success(request, "Descanso eliminado correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el descanso porque otros registros dependen de él.")
    return redirect('crud_descanso')

# 6. Entrenador
def crud_entrenador(request):
    if request.method == 'POST':
        form = EntrenadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrenador agregado exitosamente.")
            return redirect('crud_entrenador')
    else:
        form = EntrenadorForm()
    records = format_records(Entrenador.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Entrenador', 'delete_url_name': 'delete_entrenador'})

def delete_entrenador(request, pk):
    record = get_object_or_404(Entrenador, pk=pk)
    try:
        record.delete()
        messages.success(request, "Entrenador eliminado correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el entrenador porque tiene clases u otros registros a su cargo.")
    return redirect('crud_entrenador')

# 7. Usuario
def crud_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario agregado exitosamente.")
            return redirect('crud_usuario')
    else:
        form = UsuarioForm()
    records = format_records(Usuario.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Usuario', 'delete_url_name': 'delete_usuario'})

def delete_usuario(request, pk):
    record = get_object_or_404(Usuario, pk=pk)
    try:
        record.delete()
        messages.success(request, "Usuario eliminado correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el usuario porque hay registros (como rutinas o sesiones) asociados a él.")
    return redirect('crud_usuario')

# 8. Maquina
def crud_maquina(request):
    if request.method == 'POST':
        form = MaquinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Máquina agregada exitosamente.")
            return redirect('crud_maquina')
    else:
        form = MaquinaForm()
    records = format_records(Maquina.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Maquina', 'delete_url_name': 'delete_maquina'})

def delete_maquina(request, pk):
    record = get_object_or_404(Maquina, pk=pk)
    try:
        record.delete()
        messages.success(request, "Máquina eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la máquina porque hay otros registros asociados a ella.")
    return redirect('crud_maquina')

# 9. PerfilMedico
def crud_perfil_medico(request):
    if request.method == 'POST':
        form = PerfilMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil Médico agregado exitosamente.")
            return redirect('crud_perfil_medico')
    else:
        form = PerfilMedicoForm()
    records = format_records(PerfilMedico.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Perfil Medico', 'delete_url_name': 'delete_perfil_medico'})

def delete_perfil_medico(request, pk):
    record = get_object_or_404(PerfilMedico, pk=pk)
    try:
        record.delete()
        messages.success(request, "Perfil Médico eliminado correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el perfil médico porque depende de otros registros.")
    return redirect('crud_perfil_medico')

# 10. ClaseGrupal
def crud_clase_grupal(request):
    if request.method == 'POST':
        form = ClaseGrupalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Clase agregada exitosamente.")
            return redirect('crud_clase_grupal')
    else:
        form = ClaseGrupalForm()
    records = format_records(ClaseGrupal.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Clase Grupal', 'delete_url_name': 'delete_clase_grupal'})

def delete_clase_grupal(request, pk):
    record = get_object_or_404(ClaseGrupal, pk=pk)
    try:
        record.delete()
        messages.success(request, "Clase eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la clase porque existen reservas u otros registros asociados.")
    return redirect('crud_clase_grupal')

# 11. Rutina
def crud_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rutina agregada exitosamente.")
            return redirect('crud_rutina')
    else:
        form = RutinaForm()
    records = format_records(Rutina.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Rutina', 'delete_url_name': 'delete_rutina'})

def delete_rutina(request, pk):
    record = get_object_or_404(Rutina, pk=pk)
    try:
        record.delete()
        messages.success(request, "Rutina eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la rutina porque hay ejercicios de rutina asociados a ella.")
    return redirect('crud_rutina')

# 12. ReservaClase
def crud_reserva_clase(request):
    if request.method == 'POST':
        form = ReservaClaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva agregada exitosamente.")
            return redirect('crud_reserva_clase')
    else:
        form = ReservaClaseForm()
    records = format_records(ReservaClase.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Reserva Clase', 'delete_url_name': 'delete_reserva_clase'})

def delete_reserva_clase(request, pk):
    record = get_object_or_404(ReservaClase, pk=pk)
    try:
        record.delete()
        messages.success(request, "Reserva eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la reserva por dependencias foráneas.")
    return redirect('crud_reserva_clase')

# 13. SesionEntrenamiento
def crud_sesion_entrenamiento(request):
    if request.method == 'POST':
        form = SesionEntrenamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sesión de entrenamiento agregada exitosamente.")
            return redirect('crud_sesion_entrenamiento')
    else:
        form = SesionEntrenamientoForm()
    records = format_records(SesionEntrenamiento.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Sesion Entrenamiento', 'delete_url_name': 'delete_sesion_entrenamiento'})

def delete_sesion_entrenamiento(request, pk):
    record = get_object_or_404(SesionEntrenamiento, pk=pk)
    try:
        record.delete()
        messages.success(request, "Sesión de entrenamiento eliminada correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar la sesión de entrenamiento debido a conflictos de integridad de base de datos.")
    return redirect('crud_sesion_entrenamiento')

# 14. RutinaEjercicio
def crud_rutina_ejercicio(request):
    if request.method == 'POST':
        form = RutinaEjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ejercicio de rutina agregado exitosamente.")
            return redirect('crud_rutina_ejercicio')
    else:
        form = RutinaEjercicioForm()
    records = format_records(RutinaEjercicio.objects.all())
    return render(request, 'gym/crud_template.html', {'form': form, 'records': records, 'model_name': 'Rutina Ejercicio', 'delete_url_name': 'delete_rutina_ejercicio'})

def delete_rutina_ejercicio(request, pk):
    record = get_object_or_404(RutinaEjercicio, pk=pk)
    try:
        record.delete()
        messages.success(request, "Ejercicio de rutina eliminado correctamente.")
    except IntegrityError:
        messages.error(request, "No se puede eliminar el registro por conflictos de FK.")
    return redirect('crud_rutina_ejercicio')