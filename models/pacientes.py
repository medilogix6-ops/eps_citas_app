from database import get_connection


def registrar_paciente(documento, nombre, apellido, telefono, correo, eps):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (documento, nombre, apellido, telefono, correo, eps))
        conn.commit()
        return True, "Paciente registrado exitosamente."
    except Exception as e:
        if "Duplicate" in str(e):
            return False, "Ya existe un paciente con ese número de documento."
        return False, f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()


def existe_paciente(documento):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM pacientes WHERE documento = %s", (documento,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def obtener_todos():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM pacientes ORDER BY nombre, apellido")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def actualizar_paciente(documento, nombre, apellido, telefono, correo, eps):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            UPDATE pacientes
            SET nombre=%s, apellido=%s, telefono=%s, correo=%s, eps=%s
            WHERE documento=%s
        """, (nombre, apellido, telefono, correo, eps, documento))
        conn.commit()
        return True, "Paciente actualizado."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()
