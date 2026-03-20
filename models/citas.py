from database import get_connection


def reservar_cita(documento, medico_id, tipo_cita, fecha, hora, direccion_eps):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO citas (documento, medico_id, tipo_cita, fecha, hora, direccion_eps)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (documento, medico_id, tipo_cita, fecha, hora, direccion_eps))
        conn.commit()
        return True, "Cita reservada exitosamente."
    except Exception as e:
        return False, f"Error al reservar cita: {str(e)}"
    finally:
        cur.close()
        conn.close()


def consultar_citas_paciente(documento):
    """JOIN completo: paciente + médico + cita"""
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
                p.nombre        AS pac_nombre,
                p.apellido      AS pac_apellido,
                p.eps,
                m.nombre        AS medico,
                m.especialidad,
                c.id            AS cita_id,
                c.tipo_cita,
                c.fecha,
                c.hora,
                c.direccion_eps,
                c.estado
            FROM pacientes p
            INNER JOIN citas   c ON p.documento  = c.documento
            INNER JOIN medicos m ON c.medico_id  = m.id
            WHERE p.documento = %s
            ORDER BY c.fecha, c.hora
        """, (documento,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_todas_citas():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
                p.documento,
                p.nombre   AS pac_nombre,
                p.apellido AS pac_apellido,
                m.nombre   AS medico,
                m.especialidad,
                c.id       AS cita_id,
                c.tipo_cita,
                c.fecha,
                c.hora,
                c.direccion_eps,
                c.estado
            FROM citas c
            INNER JOIN pacientes p ON c.documento  = p.documento
            INNER JOIN medicos   m ON c.medico_id  = m.id
            ORDER BY c.fecha DESC, c.hora
        """)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_cita_por_id(cita_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
                c.*,
                p.nombre   AS pac_nombre,
                p.apellido AS pac_apellido,
                m.nombre   AS medico_nombre
            FROM citas c
            INNER JOIN pacientes p ON c.documento = p.documento
            INNER JOIN medicos   m ON c.medico_id = m.id
            WHERE c.id = %s
        """, (cita_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def actualizar_cita(cita_id, medico_id, tipo_cita, fecha, hora, direccion_eps, estado):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            UPDATE citas
            SET medico_id=%s, tipo_cita=%s, fecha=%s, hora=%s,
                direccion_eps=%s, estado=%s
            WHERE id=%s
        """, (medico_id, tipo_cita, fecha, hora, direccion_eps, estado, cita_id))
        conn.commit()
        return True, "Cita actualizada exitosamente."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()


def eliminar_cita(cita_id):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("DELETE FROM citas WHERE id = %s", (cita_id,))
        conn.commit()
        return True, "Cita eliminada."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def estadisticas():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
                COUNT(*)                                         AS total,
                SUM(estado = 'Pendiente')                        AS pendientes,
                SUM(estado = 'Confirmada')                       AS confirmadas,
                SUM(estado = 'Cancelada')                        AS canceladas
            FROM citas
        """)
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()
