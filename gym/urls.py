from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Original
    path('sedes/', views.listar_sedes, name='sedes'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('clases/<int:sede_id>/', views.clases_por_sede, name='clases_por_sede'),

    # CRUD
    path('crud/sede/', views.crud_sede, name='crud_sede'),
    path('crud/sede/delete/<int:pk>/', views.delete_sede, name='delete_sede'),

    path('crud/catalogo_ejercicios/', views.crud_catalogo_ejercicios, name='crud_catalogo_ejercicios'),
    path('crud/catalogo_ejercicios/delete/<int:pk>/', views.delete_catalogo_ejercicios, name='delete_catalogo_ejercicios'),

    path('crud/series/', views.crud_series, name='crud_series'),
    path('crud/series/delete/<int:pk>/', views.delete_series, name='delete_series'),

    path('crud/repeticiones/', views.crud_repeticiones, name='crud_repeticiones'),
    path('crud/repeticiones/delete/<int:pk>/', views.delete_repeticiones, name='delete_repeticiones'),

    path('crud/descanso/', views.crud_descanso, name='crud_descanso'),
    path('crud/descanso/delete/<int:pk>/', views.delete_descanso, name='delete_descanso'),

    path('crud/entrenador/', views.crud_entrenador, name='crud_entrenador'),
    path('crud/entrenador/delete/<int:pk>/', views.delete_entrenador, name='delete_entrenador'),

    path('crud/usuario/', views.crud_usuario, name='crud_usuario'),
    path('crud/usuario/delete/<int:pk>/', views.delete_usuario, name='delete_usuario'),

    path('crud/maquina/', views.crud_maquina, name='crud_maquina'),
    path('crud/maquina/delete/<int:pk>/', views.delete_maquina, name='delete_maquina'),

    path('crud/perfil_medico/', views.crud_perfil_medico, name='crud_perfil_medico'),
    path('crud/perfil_medico/delete/<int:pk>/', views.delete_perfil_medico, name='delete_perfil_medico'),

    path('crud/clase_grupal/', views.crud_clase_grupal, name='crud_clase_grupal'),
    path('crud/clase_grupal/delete/<int:pk>/', views.delete_clase_grupal, name='delete_clase_grupal'),

    path('crud/rutina/', views.crud_rutina, name='crud_rutina'),
    path('crud/rutina/delete/<int:pk>/', views.delete_rutina, name='delete_rutina'),

    path('crud/reserva_clase/', views.crud_reserva_clase, name='crud_reserva_clase'),
    path('crud/reserva_clase/delete/<int:pk>/', views.delete_reserva_clase, name='delete_reserva_clase'),

    path('crud/sesion_entrenamiento/', views.crud_sesion_entrenamiento, name='crud_sesion_entrenamiento'),
    path('crud/sesion_entrenamiento/delete/<int:pk>/', views.delete_sesion_entrenamiento, name='delete_sesion_entrenamiento'),

    path('crud/rutina_ejercicio/', views.crud_rutina_ejercicio, name='crud_rutina_ejercicio'),
    path('crud/rutina_ejercicio/delete/<int:pk>/', views.delete_rutina_ejercicio, name='delete_rutina_ejercicio'),

   
    # Consultas Especiales
path('consultas-especiales/', views.consultas_especiales, name='consultas_especiales'),
path('consulta-left-join/', views.consulta_left_join, name='consulta_left_join'),
path('consulta-inner-join/', views.consulta_inner_join, name='consulta_inner_join'),
path('consulta-group-by/', views.consulta_group_by, name='consulta_group_by'),
path('consulta-agregadas/', views.consulta_agregadas, name='consulta_agregadas'),
path('consulta-subquery/', views.consulta_subquery, name='consulta_subquery'),
path('consulta-where-order/', views.consulta_where_order, name='consulta_where_order'),
]