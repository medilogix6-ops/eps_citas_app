from database import get_connection


def listar_medicos():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id, nombre, especialidad, direccion FROM medicos ORDER BY nombre")
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
            SELECT id, nombre, especialidad, tipo_cita, direccion
            FROM medicos WHERE id = %s
            """,
            (medico_id,),
        )
        return cur.fetchone()
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
    cur  = conn.cursor()
    try:
        cur.execute("DELETE FROM medicos WHERE id = %s", (medico_id,))
        conn.commit()
        return True, "Médico eliminado."
    except Exception as e:
        if "foreign key" in str(e).lower():
            return False, "No se puede eliminar: el médico tiene citas asignadas."
        return False, str(e)
    finally:
        cur.close()
        conn.close()
