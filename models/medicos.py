from database import get_connection


def listar_medicos():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT id, nombre, especialidad, direccion, telefono
            FROM medicos ORDER BY nombre
            """
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def listar_medicos_admin():
    """Listado para administrador (tabla de consulta)."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT m.id, m.nombre, m.especialidad, m.tipo_cita, m.direccion, m.telefono
            FROM medicos m
            ORDER BY m.nombre
            """
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_medico_por_id(medico_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT id, nombre, especialidad, tipo_cita, direccion, telefono
            FROM medicos WHERE id = %s
            """,
            (medico_id,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def actualizar_medico(medico_id, nombre, especialidad, tipo_cita, direccion, telefono):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE medicos
            SET nombre = %s, especialidad = %s, tipo_cita = %s, direccion = %s, telefono = %s
            WHERE id = %s
            """,
            (nombre, especialidad, tipo_cita, direccion or None, telefono or None, medico_id),
        )
        conn.commit()
        return True, "Perfil del médico actualizado."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def agregar_medico(nombre, especialidad, direccion=''):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO medicos (nombre, especialidad, direccion) VALUES (%s, %s, %s)",
            (nombre, especialidad, direccion if direccion else None)
        )
        conn.commit()
        return True, "Médico agregado."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def eliminar_medico(medico_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM usuarios WHERE medico_id = %s", (medico_id,))
        if cur.fetchone()[0] > 0:
            return (
                False,
                "No se puede eliminar: hay un usuario vinculado a este médico. "
                "Elimine o cambie el rol de ese usuario en Usuarios.",
            )
        cur.execute("SELECT COUNT(*) FROM citas WHERE medico_id = %s", (medico_id,))
        if cur.fetchone()[0] > 0:
            return False, "No se puede eliminar: el médico tiene citas registradas."

        cur.execute("DELETE FROM medicos WHERE id = %s", (medico_id,))
        conn.commit()
        return True, "Médico eliminado."
    except Exception as e:
        if "foreign key" in str(e).lower():
            return False, "No se puede eliminar: el médico tiene datos relacionados en el sistema."
        return False, str(e)
    finally:
        cur.close()
        conn.close()
