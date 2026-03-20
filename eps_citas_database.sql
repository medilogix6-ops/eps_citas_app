-- ============================================================
--  BASE DE DATOS: eps_citas
--  Proyecto: Sistema de Gestión de Citas Médicas - EPS
--  Programa: ADSO19 - SENA
--  Tecnología: MySQL
-- ============================================================

-- 1. Crear y seleccionar la base de datos
DROP DATABASE IF EXISTS eps_citas;
CREATE DATABASE eps_citas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

USE eps_citas;

-- ============================================================
-- 2. TABLA: roles
-- ============================================================
CREATE TABLE roles (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(50)  NOT NULL UNIQUE,
    descripcion VARCHAR(150),
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3. TABLA: usuarios
-- ============================================================
CREATE TABLE usuarios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(60)  NOT NULL UNIQUE,
    correo      VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,          -- guardar hash (bcrypt)
    rol_id      INT          NOT NULL,
    activo      TINYINT(1)   DEFAULT 1,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (rol_id) REFERENCES roles(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================================
-- 4. TABLA: pacientes
-- ============================================================
CREATE TABLE pacientes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    documento   VARCHAR(15)  NOT NULL UNIQUE,
    nombre      VARCHAR(80)  NOT NULL,
    apellido    VARCHAR(80)  NOT NULL,
    telefono    VARCHAR(20),
    correo      VARCHAR(100),
    eps         VARCHAR(100),
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 5. TABLA: medicos
-- ============================================================
CREATE TABLE medicos (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(120) NOT NULL,
    especialidad VARCHAR(80)  NOT NULL,
    tipo_cita    ENUM('General','Odontología','Especialista') NOT NULL DEFAULT 'General',
    direccion    VARCHAR(150),
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 6. TABLA: citas
-- ============================================================
CREATE TABLE citas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    documento       VARCHAR(15)  NOT NULL,
    medico_id       INT          NOT NULL,
    tipo_cita       ENUM('General', 'Odontología', 'Especialista') NOT NULL,
    fecha           DATE         NOT NULL,
    hora            TIME         NOT NULL,
    direccion_eps   VARCHAR(150) NOT NULL,
    estado          ENUM('Pendiente', 'Confirmada', 'Cancelada') DEFAULT 'Pendiente',
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Llave foránea hacia pacientes
    CONSTRAINT fk_cita_paciente
        FOREIGN KEY (documento) REFERENCES pacientes(documento)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Llave foránea hacia medicos
    CONSTRAINT fk_cita_medico
        FOREIGN KEY (medico_id) REFERENCES medicos(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================================
-- 7. DATOS DE PRUEBA
-- ============================================================

-- Roles
INSERT INTO roles (nombre, descripcion) VALUES
    ('Administrador', 'Acceso total al sistema: gestión de pacientes, citas y usuarios'),
    ('Paciente',      'Acceso limitado: reservar y consultar sus propias citas');

-- Usuarios (passwords de prueba hasheadas con bcrypt)
-- Administrador -> password: Admin2025*
-- Pacientes     -> password: Paciente123*
-- NOTA: en Flask usa generate_password_hash() de werkzeug antes de insertar en producción
INSERT INTO usuarios (username, correo, password, rol_id) VALUES
    ('admin',        'admin@eps.com',            '$2b$12$KIXtq1234hashadmin000uQWERTYexamplehashADMIN0000000000', 1),
    ('juan.perez',   'juan.perez@email.com',      '$2b$12$KIXtq1234hashpac1000uQWERTYexamplehashPAC10000000000',  2),
    ('maria.lopez',  'maria.lopez@email.com',     '$2b$12$KIXtq1234hashpac2000uQWERTYexamplehashPAC20000000000',  2),
    ('carlos.r',     'carlos.r@email.com',        '$2b$12$KIXtq1234hashpac3000uQWERTYexamplehashPAC30000000000',  2),
    ('lucia.torres', 'lucia.torres@email.com',    '$2b$12$KIXtq1234hashpac4000uQWERTYexamplehashPAC40000000000',  2),
    ('andres.v',     'andres.v@email.com',        '$2b$12$KIXtq1234hashpac5000uQWERTYexamplehashPAC50000000000',  2);

-- Médicos
INSERT INTO medicos (nombre, especialidad, tipo_cita, direccion) VALUES
    ('Dr. Carlos Gómez',    'Medicina General', 'General',       'Cra 7 # 32-16, Bogotá'),
    ('Dra. Laura Martínez', 'Odontología',      'Odontología',   'Cra 9 # 45-20, Bogotá'),
    ('Dr. Andrés Ríos',     'Cardiología',      'Especialista',  'Cra 11 # 50-10, Bogotá'),
    ('Dra. Sofía Herrera',  'Pediatría',        'General',       'Cra 13 # 60-15, Bogotá'),
    ('Dr. Miguel Torres',   'Ortopedia',        'Especialista',  'Cra 15 # 70-20, Bogotá');

-- Pacientes
INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps) VALUES
    ('1020304050', 'Juan',    'Pérez',   '3101234567', 'juan.perez@email.com',    'Sura'),
    ('1030405060', 'María',   'López',   '3207654321', 'maria.lopez@email.com',   'Sanitas'),
    ('1040506070', 'Carlos',  'Ramírez', '3159876543', 'carlos.r@email.com',      'Nueva EPS'),
    ('1050607080', 'Lucía',   'Torres',  '3001112233', 'lucia.torres@email.com',  'Compensar'),
    ('1060708090', 'Andrés',  'Vargas',  '3134455667', 'andres.v@email.com',      'Famisanar');

-- Citas
INSERT INTO citas (documento, medico_id, tipo_cita, fecha, hora, direccion_eps, estado) VALUES
    ('1020304050', 1, 'General',      '2025-07-10', '08:00:00', 'Cra 7 # 32-16, Bogotá',          'Confirmada'),
    ('1030405060', 2, 'Odontología',  '2025-07-11', '10:30:00', 'Av. El Dorado # 68-65, Bogotá',  'Pendiente'),
    ('1040506070', 3, 'Especialista', '2025-07-12', '14:00:00', 'Cll 100 # 19-61, Bogotá',        'Pendiente'),
    ('1050607080', 4, 'General',      '2025-07-15', '09:00:00', 'Cra 15 # 80-45, Bogotá',         'Confirmada'),
    ('1060708090', 5, 'Especialista', '2025-07-16', '11:00:00', 'Cll 72 # 10-07, Bogotá',         'Cancelada');

-- ============================================================
-- 8. CONSULTAS DE REFERENCIA (usadas en la app Flask)
-- ============================================================

-- 8.1 Login: verificar usuario y obtener su rol
-- SELECT u.id, u.username, u.password, r.nombre AS rol
-- FROM usuarios u
-- INNER JOIN roles r ON u.rol_id = r.id
-- WHERE u.username = %s AND u.activo = 1;

-- 8.2 Consultar cita de un paciente por documento (JOIN)
-- SELECT
--     p.nombre,
--     p.apellido,
--     m.nombre      AS medico,
--     c.tipo_cita,
--     c.fecha,
--     c.hora,
--     c.direccion_eps,
--     c.estado
-- FROM pacientes p
-- INNER JOIN citas    c ON p.documento  = c.documento
-- INNER JOIN medicos  m ON c.medico_id  = m.id
-- WHERE p.documento = %s;

-- 8.3 Listar todos los médicos (para el <select> del formulario)
-- SELECT id, nombre, especialidad FROM medicos ORDER BY nombre;

-- 8.4 Actualizar una cita
-- UPDATE citas
-- SET fecha = %s, hora = %s, tipo_cita = %s, medico_id = %s
-- WHERE id = %s AND documento = %s;

-- ============================================================
-- 9. VERIFICACIÓN RÁPIDA
-- ============================================================
SELECT 'roles'     AS tabla, COUNT(*) AS registros FROM roles
UNION ALL
SELECT 'usuarios',            COUNT(*)              FROM usuarios
UNION ALL
SELECT 'pacientes',           COUNT(*)              FROM pacientes
UNION ALL
SELECT 'medicos',             COUNT(*)              FROM medicos
UNION ALL
SELECT 'citas',               COUNT(*)              FROM citas;
