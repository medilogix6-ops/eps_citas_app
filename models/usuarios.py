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
            SELECT u.id, u.username, u.correo, u.password, r.nombre AS rol
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


def registrar_usuario(username, correo, password, rol_id=2):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute("""
            INSERT INTO usuarios (username, correo, password, rol_id)
            VALUES (%s, %s, %s, %s)
        """, (username, correo, hashed, rol_id))
        conn.commit()
        return True, "Usuario registrado."
    except Exception as e:
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
            SELECT u.id, u.username, u.correo, u.rol_id, r.nombre AS rol, u.activo, u.created_at
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
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
            SELECT u.id, u.username, u.correo, u.rol_id, r.nombre AS rol, u.activo, u.created_at
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            WHERE u.id = %s
        """, (user_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def actualizar_usuario(user_id, username, correo, rol_id, password=None):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        if password:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            cur.execute(
                """
                UPDATE usuarios
                SET username = %s, correo = %s, rol_id = %s, password = %s
                WHERE id = %s
                """,
                (username, correo, rol_id, hashed, user_id)
            )
        else:
            cur.execute(
                """
                UPDATE usuarios
                SET username = %s, correo = %s, rol_id = %s
                WHERE id = %s
                """,
                (username, correo, rol_id, user_id)
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
