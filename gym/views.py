from django.shortcuts import render
from django.db import connection


# Create your views here.
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