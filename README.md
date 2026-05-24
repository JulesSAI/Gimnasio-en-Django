# Proyecto Gimnasio - Sistema de Gestión para Bases de Datos

Este proyecto es una aplicación web desarrollada con Django y PostgreSQL para administrar un gimnasio. Incluye tablas como `SEDE`, `USUARIO`, `ENTRENADOR`, `CLASE_GRUPAL`, `RUTINA`, entre otras.

## Requisitos previos

- Python 3.8 o superior
- PostgreSQL (con pgAdmin opcional)
- Git (para clonar el repositorio)

## Instalación y configuración paso a paso

Sigue estas instrucciones para ejecutar el proyecto en tu máquina local.

## Crear y activar un entorno virtual

Windows:

python -m venv env
env\Scripts\activate

macOS/Linux:
python3 -m venv env
source env/bin/activate

## Instalar dependencias

pip install -r requirements.txt

## Instalar dependencias

El proyecto usa python-decouple para gestionar la configuración sensible. Debes crear un archivo .env en la raíz del proyecto (junto a manage.py) con el siguiente contenido:

DB_NAME=gym_db               # o el nombre que hayas usado en tu dump
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

Nota: Reemplaza tu_contraseña con la contraseña de tu usuario postgres. Si no tienes contraseña, déjala vacío: DB_PASSWORD=.

## Crear la base de datos en PostgreSQL

Abre pgAdmin o la terminal psql y ejecuta:

CREATE DATABASE gym_db;

Asegúrate de que el nombre coincida con el que pusiste en el .env.

El repositorio incluye un archivo dump_gym_db1_2.sql, realiza la consulta y carga las tablas


## Aplicar las migraciones de Django (tablas internas)

python manage.py migrate

Esto crea las tablas necesarias para el admin de Django (auth_user, django_session, etc.).


## Crea un superusuario 

python manage.py createsuperuser

## Ejeccuta el servidor de desarrollo

python manage.py runserver

Abre tu navegador en http://127.0.0.1:8000/sedes/ para ver la lista de sedes.


## Ejeccuta el servidor de Docker

```
docker-compose up --build  
```



# Estructura del proyecto

gym/: aplicación principal con vistas (SQL crudo) y plantillas.

proyecto_gimnasio/: configuración del proyecto.

dump_gym_db1_2.sql: volcado inicial de la base de datos.

requirements.txt: dependencias de Python.

.env: configuración local (no se sube al repositorio).

# Consultas SQL implementadas

Todas las vistas utilizan consultas SQL escritas directamente con connection.cursor()