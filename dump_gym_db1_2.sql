-- ==============================================================================
-- 0. CREACIÓN DE BASE DE DATOS
-- ==============================================================================
-- CREATE DATABASE db_gimnasio_fase3;

-- ==============================================================================
-- 1. TABLAS INDEPENDIENTES (Sin llaves foráneas)
-- ==============================================================================

CREATE TABLE SEDE (
    id_sede SERIAL PRIMARY KEY,
    nombre_sede VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    capacidad_maxima_personas INT CHECK (capacidad_maxima_personas > 0),
    coordenadas_gps VARCHAR(100)
);

CREATE TABLE CATALOGO_EJERCICIOS (
    id_ejercicio SERIAL PRIMARY KEY,
    nombre_ejercicio VARCHAR(150) NOT NULL,
    grupo_muscular_principal VARCHAR(100),
    tipo_ejercicio VARCHAR(50), 
    url_video_tutorial VARCHAR(255)
);

CREATE TABLE SERIES (
    id_serie SERIAL PRIMARY KEY,
    cantidad_series INT NOT NULL UNIQUE CHECK (cantidad_series > 0)
);

CREATE TABLE REPETICIONES (
    id_repeticion SERIAL PRIMARY KEY,
    cantidad_repeticiones INT NOT NULL UNIQUE CHECK (cantidad_repeticiones > 0)
);

CREATE TABLE DESCANSO (
    id_descanso SERIAL PRIMARY KEY,
    tiempo_segundos INT NOT NULL UNIQUE CHECK (tiempo_segundos >= 0)
);

-- ==============================================================================
-- 2. TABLAS DE PRIMER NIVEL (Dependen directamente de SEDE)
-- ==============================================================================

CREATE TABLE ENTRENADOR (
    id_entrenador SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    anios_experiencia INT CHECK (anios_experiencia >= 0),
    id_sede_base INT NOT NULL,
    FOREIGN KEY (id_sede_base) REFERENCES SEDE(id_sede)
);

CREATE TABLE USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    estado_suscripcion VARCHAR(50) DEFAULT 'Activo', 
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_sede_principal INT,
    FOREIGN KEY (id_sede_principal) REFERENCES SEDE(id_sede)
);

CREATE TABLE MAQUINA (
    id_maquina SERIAL PRIMARY KEY,
    nombre_maquina VARCHAR(100) NOT NULL,
    marca VARCHAR(100),
    estado_mantenimiento VARCHAR(50) DEFAULT 'Operativa', 
    id_sede INT NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES SEDE(id_sede)
);

-- ==============================================================================
-- 3. TABLAS DE SEGUNDO NIVEL (Dependen de Usuario o Entrenador)
-- ==============================================================================

CREATE TABLE PERFIL_MEDICO (
    id_perfil SERIAL PRIMARY KEY,
    id_usuario INT UNIQUE NOT NULL, 
    grupo_sanguineo VARCHAR(5),
    alergias TEXT, 
    lesiones_previas TEXT,
    peso_actual_kg NUMERIC(5,2) CHECK (peso_actual_kg > 0),
    porcentaje_grasa NUMERIC(5,2) CHECK (porcentaje_grasa >= 0 AND porcentaje_grasa <= 100),
    objetivo_fisico VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

CREATE TABLE CLASE_GRUPAL (
    id_clase SERIAL PRIMARY KEY,
    nombre_clase VARCHAR(100) NOT NULL,
    fecha_hora_inicio TIMESTAMP NOT NULL,
    fecha_hora_fin TIMESTAMP NOT NULL,
    capacidad_maxima INT NOT NULL CHECK (capacidad_maxima > 0),
    id_sede INT NOT NULL,
    id_entrenador INT NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES SEDE(id_sede),
    FOREIGN KEY (id_entrenador) REFERENCES ENTRENADOR(id_entrenador)
);

CREATE TABLE RUTINA (
    id_rutina SERIAL PRIMARY KEY,
    nivel_dificultad VARCHAR(50),
    estado_rutina VARCHAR(50) DEFAULT 'Activa',
    id_usuario INT NOT NULL,
    id_entrenador INT, 
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_entrenador) REFERENCES ENTRENADOR(id_entrenador)
);

-- ==============================================================================
-- 4. TABLAS DE TERCER NIVEL (Transaccionales e Intermedias)
-- ==============================================================================

CREATE TABLE RESERVA_CLASE (
    id_reserva SERIAL PRIMARY KEY,
    fecha_hora_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_reserva VARCHAR(50) DEFAULT 'Confirmada', 
    id_clase INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_clase) REFERENCES CLASE_GRUPAL(id_clase),
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

CREATE TABLE SESION_ENTRENAMIENTO (
    id_sesion SERIAL PRIMARY KEY,
    fecha_hora_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duracion_minutos INT CHECK (duracion_minutos > 0),
    metricas_registradas TEXT, 
    id_usuario INT NOT NULL,
    id_sede INT NOT NULL,
    id_rutina INT, 
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_sede) REFERENCES SEDE(id_sede),
    FOREIGN KEY (id_rutina) REFERENCES RUTINA(id_rutina)
);

CREATE TABLE RUTINA_EJERCICIO (
    id_rutina_ejercicio SERIAL PRIMARY KEY,
    id_rutina INT NOT NULL,
    id_ejercicio INT NOT NULL,
    id_serie INT NOT NULL,
    id_repeticion INT NOT NULL,
    id_descanso INT NOT NULL,
    FOREIGN KEY (id_rutina) REFERENCES RUTINA(id_rutina) ON DELETE CASCADE,
    FOREIGN KEY (id_ejercicio) REFERENCES CATALOGO_EJERCICIOS(id_ejercicio),
    FOREIGN KEY (id_serie) REFERENCES SERIES(id_serie),
    FOREIGN KEY (id_repeticion) REFERENCES REPETICIONES(id_repeticion),
    FOREIGN KEY (id_descanso) REFERENCES DESCANSO(id_descanso)
);

-- ==============================================================================
-- 5. INSERCIÓN DE DATOS DE PRUEBA
-- ==============================================================================

-- 5.1 Inserción en SEDE
INSERT INTO SEDE (nombre_sede, ciudad, direccion, capacidad_maxima_personas, coordenadas_gps) VALUES
('Sede Norte', 'Bogotá', 'Calle 170 # 45-20', 500, '4.755,-74.045'),
('Sede Chapinero', 'Bogotá', 'Carrera 13 # 60-15', 300, '4.646,-74.062'),
('Sede Poblado', 'Medellín', 'Carrera 43A # 1-50', 400, '6.208,-75.567'),
('Sede Laureles', 'Medellín', 'Avenida 33 # 74B-06', 350, '6.242,-75.591'),
('Sede Ciudad Jardín', 'Cali', 'Calle 16 # 100-20', 450, '3.367,-76.530'),
('Sede Granada', 'Cali', 'Avenida 9 Norte # 14N-45', 250, '3.456,-76.536'),
('Sede Alto Prado', 'Barranquilla', 'Carrera 53 # 79-20', 380, '11.002,-74.809'),
('Sede Cabecera', 'Bucaramanga', 'Carrera 33 # 48-10', 300, '7.118,-73.112'),
('Sede Bocagrande', 'Cartagena', 'Carrera 2 # 5-60', 200, '10.400,-75.553'),
('Sede Centro', 'Pereira', 'Calle 19 # 6-40', 280, '4.814,-75.696');

-- 5.2 Inserción en CATALOGO_EJERCICIOS
INSERT INTO CATALOGO_EJERCICIOS (nombre_ejercicio, grupo_muscular_principal, tipo_ejercicio) VALUES
('Press de Banca', 'Pecho', 'Fuerza'),
('Sentadilla Libre', 'Pierna', 'Fuerza'),
('Peso Muerto', 'Espalda', 'Fuerza'),
('Dominadas', 'Espalda', 'Fuerza'),
('Press Militar', 'Hombro', 'Fuerza'),
('Curl de Bíceps', 'Brazo', 'Fuerza'),
('Extensión de Tríceps', 'Brazo', 'Fuerza'),
('Plancha Abdominal', 'Core', 'Resistencia'),
('Burpees', 'Cuerpo Completo', 'Cardio'),
('Cinta de Correr', 'Pierna', 'Cardio');

-- 5.3 Inserción en SERIES, REPETICIONES Y DESCANSO
INSERT INTO SERIES (cantidad_series) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
INSERT INTO REPETICIONES (cantidad_repeticiones) VALUES (1), (5), (8), (10), (12), (15), (20), (25), (30), (50);
INSERT INTO DESCANSO (tiempo_segundos) VALUES (0), (30), (45), (60), (90), (120), (150), (180), (240), (300);

-- 5.4 Inserción en ENTRENADOR
INSERT INTO ENTRENADOR (nombres, apellidos, especialidad, anios_experiencia, id_sede_base) VALUES
('Carlos', 'Ramírez', 'Hipertrofia', 5, 1),
('Ana', 'Gómez', 'Crossfit', 3, 2),
('Luis', 'Martínez', 'Rehabilitación', 8, 3),
('Marta', 'López', 'Yoga', 4, 4),
('Jorge', 'Díaz', 'Fuerza', 6, 5),
('Laura', 'Pérez', 'Pilates', 2, 6),
('Diego', 'Hernández', 'Hipertrofia', 7, 7),
('Sofía', 'García', 'Zumba', 3, 8),
('Andrés', 'Fernández', 'Nutrición', 5, 9),
('Elena', 'Ruiz', 'Crossfit', 4, 10);

-- 5.5 Inserción en USUARIO
INSERT INTO USUARIO (nombres, apellidos, email, id_sede_principal) VALUES
('Pedro', 'Alvarez', 'pedro.a@mail.com', 1),
('Maria', 'Bermudez', 'maria.b@mail.com', 2),
('Juan', 'Castro', 'juan.c@mail.com', 3),
('Diana', 'Delgado', 'diana.d@mail.com', 4),
('Esteban', 'Escobar', 'esteban.e@mail.com', 5),
('Camila', 'Franco', 'camila.f@mail.com', 6),
('Mateo', 'Gallego', 'mateo.g@mail.com', 7),
('Valentina', 'Herrera', 'valentina.h@mail.com', 8),
('Felipe', 'Iglesias', 'felipe.i@mail.com', 9),
('Lucia', 'Jimenez', 'lucia.j@mail.com', 10);

-- 5.6 Inserción en MAQUINA
INSERT INTO MAQUINA (nombre_maquina, marca, id_sede) VALUES
('Caminadora T100', 'LifeFitness', 1),
('Elíptica Pro', 'Technogym', 2),
('Prensa de Piernas', 'Precor', 3),
('Polea Cruzada', 'Matrix', 4),
('Máquina de Remo', 'Concept2', 5),
('Banco Plano', 'Rogue', 6),
('Silla Romana', 'Cybex', 7),
('Bicicleta Estática', 'LifeFitness', 8),
('Máquina Smith', 'Technogym', 9),
('Extensión Cuádriceps', 'Precor', 10);

-- 5.7 Inserción en PERFIL_MEDICO
INSERT INTO PERFIL_MEDICO (id_usuario, grupo_sanguineo, peso_actual_kg, porcentaje_grasa, objetivo_fisico) VALUES
(1, 'O+', 75.5, 18.2, 'Ganancia muscular'),
(2, 'A+', 62.0, 22.5, 'Pérdida de peso'),
(3, 'B-', 80.1, 15.0, 'Mantenimiento'),
(4, 'O-', 55.3, 20.1, 'Tonificación'),
(5, 'AB+', 90.0, 25.4, 'Pérdida de peso'),
(6, 'A-', 65.2, 19.8, 'Ganancia de fuerza'),
(7, 'O+', 78.9, 14.5, 'Hipertrofia'),
(8, 'B+', 58.4, 21.0, 'Mejorar resistencia'),
(9, 'A+', 85.0, 16.5, 'Rendimiento deportivo'),
(10, 'AB-', 60.5, 18.0, 'Tonificación general');

-- 5.8 Inserción en CLASE_GRUPAL
INSERT INTO CLASE_GRUPAL (nombre_clase, fecha_hora_inicio, fecha_hora_fin, capacidad_maxima, id_sede, id_entrenador) VALUES
('Yoga Matutino', '2026-06-01 06:00:00', '2026-06-01 07:00:00', 20, 1, 4),
('Crossfit WOD', '2026-06-01 18:00:00', '2026-06-01 19:00:00', 15, 2, 2),
('Zumba Party', '2026-06-02 19:00:00', '2026-06-02 20:00:00', 25, 3, 8),
('Pilates Core', '2026-06-03 07:00:00', '2026-06-03 08:00:00', 15, 4, 6),
('Spinning Avanzado', '2026-06-04 18:30:00', '2026-06-04 19:30:00', 20, 5, 5),
('HIIT Express', '2026-06-05 06:30:00', '2026-06-05 07:15:00', 10, 6, 1),
('Levantamiento Olímpico', '2026-06-06 10:00:00', '2026-06-06 11:30:00', 12, 7, 7),
('Stretching', '2026-06-07 09:00:00', '2026-06-07 10:00:00', 20, 8, 4),
('Funcional', '2026-06-08 19:00:00', '2026-06-08 20:00:00', 18, 9, 10),
('Kickboxing', '2026-06-09 20:00:00', '2026-06-09 21:00:00', 15, 10, 2);

-- 5.9 Inserción en RUTINA
INSERT INTO RUTINA (nivel_dificultad, id_usuario, id_entrenador) VALUES
('Intermedio', 1, 1),
('Principiante', 2, 2),
('Avanzado', 3, 3),
('Principiante', 4, 4),
('Intermedio', 5, 5),
('Avanzado', 6, 6),
('Intermedio', 7, 7),
('Principiante', 8, 8),
('Avanzado', 9, 9),
('Intermedio', 10, 10);

-- 5.10 Inserción en RESERVA_CLASE
INSERT INTO RESERVA_CLASE (id_clase, id_usuario) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
(6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

-- 5.11 Inserción en SESION_ENTRENAMIENTO
INSERT INTO SESION_ENTRENAMIENTO (duracion_minutos, metricas_registradas, id_usuario, id_sede, id_rutina) VALUES
(60, '{"calorias": 400, "esfuerzo": 7}', 1, 1, 1),
(45, '{"calorias": 250, "esfuerzo": 5}', 2, 2, 2),
(90, '{"calorias": 700, "esfuerzo": 9}', 3, 3, 3),
(50, '{"calorias": 300, "esfuerzo": 6}', 4, 4, 4),
(75, '{"calorias": 500, "esfuerzo": 8}', 5, 5, 5),
(60, '{"calorias": 450, "esfuerzo": 8}', 6, 6, 6),
(80, '{"calorias": 600, "esfuerzo": 7}', 7, 7, 7),
(40, '{"calorias": 200, "esfuerzo": 4}', 8, 8, 8),
(120, '{"calorias": 900, "esfuerzo": 10}', 9, 9, 9),
(60, '{"calorias": 350, "esfuerzo": 6}', 10, 10, 10);

-- 5.12 Inserción en RUTINA_EJERCICIO
INSERT INTO RUTINA_EJERCICIO (id_rutina, id_ejercicio, id_serie, id_repeticion, id_descanso) VALUES
(1, 1, 3, 4, 4), 
(2, 2, 3, 5, 4), 
(3, 3, 4, 3, 5), 
(4, 8, 3, 6, 2), 
(5, 5, 4, 4, 4), 
(6, 4, 5, 4, 4), 
(7, 6, 3, 5, 3), 
(8, 10, 1, 7, 1), 
(9, 7, 4, 4, 3), 
(10, 9, 4, 5, 2);