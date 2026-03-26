import bcrypt
from database import get_connection


def login(username: str, password: str):
    """
    Verifica credenciales.
    Retorna dict con datos del usuario o None si falla.
    """
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT u.id, u.username, u.correo, u.password, u.medico_id, r.nombre AS rol
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            WHERE u.username = %s AND u.activo = 1
        """, (username,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            user.pop('password')
            return user
        return None
    finally:
        cur.close()
        conn.close()


def listar_roles():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id, nombre, descripcion FROM roles ORDER BY id")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_rol_id_por_nombre(nombre: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id FROM roles WHERE nombre = %s", (nombre,))
        row = cur.fetchone()
        return row["id"] if row else None
    finally:
        cur.close()
        conn.close()


def registrar_usuario(username, correo, password, rol_id=2, medico_id=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute(
            """
            INSERT INTO usuarios (username, correo, password, rol_id, medico_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, correo, hashed, rol_id, medico_id),
        )
        conn.commit()
        return True, "Usuario registrado."
    except Exception as e:
        if "Duplicate" in str(e):
            return False, "El usuario o correo ya existe."
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def crear_usuario_medico(
    username, correo, password, nombre_medico, especialidad, tipo_cita, direccion_hospital, telefono=None
):
    """
    Crea fila en medicos y usuario con rol Medico vinculado.
    direccion_hospital suele ser IPS Clinica Meira Del Mar.
    """
    rid = obtener_rol_id_por_nombre("Medico")
    if not rid:
        return False, "El rol Médico no existe en la base de datos."

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO medicos (nombre, especialidad, tipo_cita, direccion, telefono)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre_medico, especialidad, tipo_cita, direccion_hospital, telefono or None),
        )
        mid = cur.lastrowid
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute(
            """
            INSERT INTO usuarios (username, correo, password, rol_id, medico_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, correo, hashed, rid, mid),
        )
        conn.commit()
        return True, "Usuario médico creado correctamente."
    except Exception as e:
        conn.rollback()
        if "Duplicate" in str(e):
            return False, "El usuario o correo ya existe."
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def listar_usuarios():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT u.id, u.username, u.correo, u.rol_id, u.medico_id,
                   r.nombre AS rol, u.activo, u.created_at,
                   m.nombre AS medico_nombre, m.especialidad AS medico_especialidad
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            LEFT JOIN medicos m ON u.medico_id = m.id
            ORDER BY u.created_at DESC
        """)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_usuario_por_id(user_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT u.id, u.username, u.correo, u.rol_id, u.medico_id,
                   r.nombre AS rol, u.activo, u.created_at,
                   m.nombre AS medico_nombre, m.especialidad AS medico_especialidad,
                   m.tipo_cita AS medico_tipo_cita, m.direccion AS medico_direccion
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            LEFT JOIN medicos m ON u.medico_id = m.id
            WHERE u.id = %s
        """, (user_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def actualizar_usuario(user_id, username, correo, rol_id, password=None, limpiar_medico_id=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        mid_sql = ", medico_id = NULL" if limpiar_medico_id else ""
        if password:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            cur.execute(
                f"""
                UPDATE usuarios
                SET username = %s, correo = %s, rol_id = %s, password = %s{mid_sql}
                WHERE id = %s
                """,
                (username, correo, rol_id, hashed, user_id),
            )
        else:
            cur.execute(
                f"""
                UPDATE usuarios
                SET username = %s, correo = %s, rol_id = %s{mid_sql}
                WHERE id = %s
                """,
                (username, correo, rol_id, user_id),
            )
        conn.commit()
        return True, "Usuario actualizado."
    except Exception as e:
        if "Duplicate" in str(e):
            return False, "El usuario o correo ya existe."
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def toggle_activo(user_id):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("UPDATE usuarios SET activo = NOT activo WHERE id = %s", (user_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def eliminar_usuario(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        if cur.rowcount == 0:
            return False, "Usuario no encontrado."
        conn.commit()
        return True, "Usuario eliminado."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()
