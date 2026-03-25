import mysql.connector
from config import Config


def _migrate_legacy_schema(cur, conn):
    """Actualiza esquemas creados antes del rol Médico e historia clínica."""
    cur.execute("SELECT DATABASE()")
    row = cur.fetchone()
    db = row[0] if row else None
    if not db:
        return

    try:
        cur.execute(
            """
            SELECT COUNT(*) FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'medico_id'
            """,
            (db,),
        )
        if cur.fetchone()[0] == 0:
            cur.execute(
                """
                ALTER TABLE usuarios
                ADD COLUMN medico_id INT NULL,
                ADD UNIQUE KEY uq_usuario_medico_id (medico_id)
                """
            )
            cur.execute(
                """
                ALTER TABLE usuarios
                ADD CONSTRAINT fk_usuario_medico
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
                ON UPDATE CASCADE ON DELETE SET NULL
                """
            )
    except Exception as e:
        print(f"migrate usuarios.medico_id: {e}")

    try:
        cur.execute("SELECT COUNT(*) FROM roles WHERE nombre = 'Medico'")
        if cur.fetchone()[0] == 0:
            cur.execute(
                """
                INSERT INTO roles (nombre, descripcion) VALUES
                ('Medico', 'Atender citas y consultar pacientes asignados')
                """
            )
    except Exception as e:
        print(f"migrate rol Medico: {e}")

    try:
        cur.execute(
            """
            ALTER TABLE citas MODIFY COLUMN estado
            ENUM('Pendiente','Confirmada','Cancelada','Atendida') DEFAULT 'Pendiente'
            """
        )
    except Exception as e:
        print(f"migrate citas.estado: {e}")

    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS historia_clinica (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                cita_id     INT NOT NULL,
                medico_id   INT NOT NULL,
                documento   VARCHAR(15) NOT NULL,
                notas       TEXT NOT NULL,
                tipo        VARCHAR(50) DEFAULT 'Control',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_hist_cita
                    FOREIGN KEY (cita_id) REFERENCES citas(id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                CONSTRAINT fk_hist_medico
                    FOREIGN KEY (medico_id) REFERENCES medicos(id)
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                CONSTRAINT fk_hist_paciente
                    FOREIGN KEY (documento) REFERENCES pacientes(documento)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
            """
        )
    except Exception as e:
        print(f"migrate historia_clinica: {e}")

    conn.commit()


def get_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
    )


def init_db():
    """
    Crea la base de datos y las tablas si no existen.
    Ejecuta el script SQL completo (eps_citas_database.sql) en Railway
    o usa sentencias individuales cuando la DB ya está creada.
    """
    import os, bcrypt

    # --- 1. Conectar sin seleccionar DB para poder crearla ---
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset='utf8mb4',
    )
    cur = conn.cursor()

    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    cur.execute(f"USE `{Config.MYSQL_DB}`;")

    # --- 2. Tablas (medicos antes que usuarios por FK medico_id) ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            nombre      VARCHAR(50)  NOT NULL UNIQUE,
            descripcion VARCHAR(150),
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicos (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            nombre       VARCHAR(120) NOT NULL,
            especialidad VARCHAR(80)  NOT NULL,
            tipo_cita    ENUM('General','Odontología','Especialista') NOT NULL DEFAULT 'General',
            direccion    VARCHAR(150),
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            username   VARCHAR(60)  NOT NULL UNIQUE,
            correo     VARCHAR(100) NOT NULL UNIQUE,
            password   VARCHAR(255) NOT NULL,
            rol_id     INT NOT NULL,
            medico_id  INT NULL,
            activo     TINYINT(1) DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_usuario_rol
                FOREIGN KEY (rol_id) REFERENCES roles(id)
                ON UPDATE CASCADE ON DELETE RESTRICT,
            CONSTRAINT fk_usuario_medico
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
                ON UPDATE CASCADE ON DELETE SET NULL,
            UNIQUE KEY uq_usuario_medico_id (medico_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            documento  VARCHAR(15)  NOT NULL UNIQUE,
            nombre     VARCHAR(80)  NOT NULL,
            apellido   VARCHAR(80)  NOT NULL,
            telefono   VARCHAR(20),
            correo     VARCHAR(100),
            eps        VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            documento     VARCHAR(15)  NOT NULL,
            medico_id     INT NOT NULL,
            tipo_cita     ENUM('General','Odontología','Especialista') NOT NULL,
            fecha         DATE NOT NULL,
            hora          TIME NOT NULL,
            direccion_eps VARCHAR(150) NOT NULL,
            estado        ENUM('Pendiente','Confirmada','Cancelada','Atendida') DEFAULT 'Pendiente',
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_cita_paciente
                FOREIGN KEY (documento) REFERENCES pacientes(documento)
                ON UPDATE CASCADE ON DELETE RESTRICT,
            CONSTRAINT fk_cita_medico
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS historia_clinica (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            cita_id     INT NOT NULL,
            medico_id   INT NOT NULL,
            documento   VARCHAR(15) NOT NULL,
            notas       TEXT NOT NULL,
            tipo        VARCHAR(50) DEFAULT 'Control',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_hist_cita
                FOREIGN KEY (cita_id) REFERENCES citas(id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            CONSTRAINT fk_hist_medico
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
                ON UPDATE CASCADE ON DELETE RESTRICT,
            CONSTRAINT fk_hist_paciente
                FOREIGN KEY (documento) REFERENCES pacientes(documento)
                ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)

    conn.commit()

    # --- 2b. Migraciones en bases ya existentes (sin medico_id, enum antiguo, etc.) ---
    _migrate_legacy_schema(cur, conn)

    # --- 3. Seed data (solo si las tablas están vacías) ---
    cur.execute("SELECT COUNT(*) FROM roles;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO roles (nombre, descripcion) VALUES
            ('Administrador', 'Acceso total al sistema'),
            ('Paciente',      'Reservar y consultar sus citas'),
            ('Medico',        'Atender citas y consultar pacientes asignados');
        """)

        admin_hash = bcrypt.hashpw(b'Admin2025*', bcrypt.gensalt()).decode()
        pac_hash   = bcrypt.hashpw(b'Paciente123*', bcrypt.gensalt()).decode()

        cur.executemany(
            "INSERT INTO usuarios (username, correo, password, rol_id) VALUES (%s,%s,%s,%s)",
            [
                ('admin',        'admin@eps.com',         admin_hash, 1),
                ('juan.perez',   'juan.perez@email.com',  pac_hash,   2),
                ('maria.lopez',  'maria.lopez@email.com', pac_hash,   2),
                ('carlos.r',     'carlos.r@email.com',    pac_hash,   2),
                ('lucia.torres', 'lucia.torres@email.com',pac_hash,   2),
                ('andres.v',     'andres.v@email.com',    pac_hash,   2),
            ]
        )

        cur.executemany(
            "INSERT INTO medicos (nombre, especialidad, tipo_cita, direccion) VALUES (%s,%s,%s,%s)",
            [
                ('Dr. Carlos Gómez',    'Medicina General', 'General',       'Cra 7 # 32-16, Bogotá'),
                ('Dra. Laura Martínez', 'Odontología',      'Odontología',   'Cra 9 # 45-20, Bogotá'),
                ('Dr. Andrés Ríos',     'Cardiología',      'Especialista',  'Cra 11 # 50-10, Bogotá'),
                ('Dra. Sofía Herrera',  'Pediatría',        'General',       'Cra 13 # 60-15, Bogotá'),
                ('Dr. Miguel Torres',   'Ortopedia',        'Especialista',  'Cra 15 # 70-20, Bogotá'),
            ]
        )

        cur.executemany(
            "INSERT INTO pacientes (documento,nombre,apellido,telefono,correo,eps) VALUES (%s,%s,%s,%s,%s,%s)",
            [
                ('1020304050','Juan',   'Pérez',   '3101234567','juan.perez@email.com',   'Sura'),
                ('1030405060','María',  'López',   '3207654321','maria.lopez@email.com',  'Sanitas'),
                ('1040506070','Carlos', 'Ramírez', '3159876543','carlos.r@email.com',     'Nueva EPS'),
                ('1050607080','Lucía',  'Torres',  '3001112233','lucia.torres@email.com', 'Compensar'),
                ('1060708090','Andrés', 'Vargas',  '3134455667','andres.v@email.com',     'Famisanar'),
            ]
        )

        cur.executemany(
            "INSERT INTO citas (documento,medico_id,tipo_cita,fecha,hora,direccion_eps,estado) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            [
                ('1020304050',1,'General',     '2026-07-10','08:00:00','Cra 7 # 32-16, Bogotá',         'Confirmada'),
                ('1030405060',2,'Odontología', '2026-07-11','10:30:00','Av. El Dorado # 68-65, Bogotá', 'Pendiente'),
                ('1040506070',3,'Especialista','2026-07-12','14:00:00','Cll 100 # 19-61, Bogotá',       'Pendiente'),
                ('1050607080',4,'General',     '2026-07-15','09:00:00','Cra 15 # 80-45, Bogotá',        'Confirmada'),
                ('1060708090',5,'Especialista','2026-07-16','11:00:00','Cll 72 # 10-07, Bogotá',        'Cancelada'),
            ]
        )

        conn.commit()
        print("✅ Datos de prueba insertados.")

    # --- 4. Asegurar que las credenciales de prueba sigan funcionando ---
    # Si el proyecto se cargó desde el script SQL de ejemplo, los hashes
    # de contraseña pueden ser placeholders y no validarán con bcrypt.
    # Aquí los reemplazamos con hashes reales solo para los usuarios de demo.
    def _fix_demo_password(username, plain_password):
        cur.execute("SELECT password FROM usuarios WHERE username = %s", (username,))
        row = cur.fetchone()
        if not row:
            return
        stored = row[0]
        # Identificador de los hashes comprados en eps_citas_database.sql
        if isinstance(stored, str) and stored.startswith('$2b$12$KIXtq1234hash'):
            new_hash = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
            cur.execute("UPDATE usuarios SET password = %s WHERE username = %s", (new_hash, username))

    _fix_demo_password('admin', 'Admin2025*')
    _fix_demo_password('juan.perez', 'Paciente123*')
    _fix_demo_password('maria.lopez', 'Paciente123*')
    _fix_demo_password('carlos.r', 'Paciente123*')
    _fix_demo_password('lucia.torres', 'Paciente123*')
    _fix_demo_password('andres.v', 'Paciente123*')
    conn.commit()

    cur.close()
    conn.close()
    print("✅ Base de datos lista.")
