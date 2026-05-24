from django.urls import path
from . import views

urlpatterns = [
    path('sedes/', views.listar_sedes, name='sedes'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('clases/<int:sede_id>/', views.clases_por_sede, name='clases_por_sede'),
]