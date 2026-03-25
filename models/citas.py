from database import get_connection
from datetime import datetime, timedelta


def reservar_cita(documento, medico_id, tipo_cita, fecha):
    """Reservar cita sin hora ni dirección (se obtienen del médico)"""
    conn = get_connection()
    cur  = conn.cursor()
    try:
        # Obtener dirección del médico
        cur.execute("SELECT direccion FROM medicos WHERE id = %s", (medico_id,))
        result = cur.fetchone()
        if not result:
            return False, "Médico no encontrado."
        direccion_eps = result[0]
        
        cur.execute("""
            INSERT INTO citas (documento, medico_id, tipo_cita, fecha, hora, direccion_eps)
            VALUES (%s, %s, %s, %s, '08:00', %s)
        """, (documento, medico_id, tipo_cita, fecha, direccion_eps))
        conn.commit()
        return True, "Cita reservada exitosamente."
    except Exception as e:
        return False, f"Error al reservar cita: {str(e)}"
    finally:
        cur.close()
        conn.close()


def obtener_medicos_por_tipo(tipo_cita):
    """Obtener médicos disponibles para un tipo de cita específico"""
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT id, nombre, especialidad, direccion 
            FROM medicos 
            WHERE tipo_cita = %s 
            ORDER BY nombre
        """, (tipo_cita,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_fechas_disponibles(medico_id, dias=30):
    """Obtener fechas disponibles (máx 3 pacientes por día) para un médico"""
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        fechas_disponibles = []
        hoy = datetime.now().date()
        
        for i in range(dias):
            fecha = hoy + timedelta(days=i)
            
            # Contar citas para ese médico en esa fecha
            cur.execute("""
                SELECT COUNT(*) as count FROM citas 
                WHERE medico_id = %s AND fecha = %s AND estado != 'Cancelada'
            """, (medico_id, fecha))
            result = cur.fetchone()
            count = result['count'] if result else 0
            
            # Si tiene menos de 3 citas, está disponible
            if count < 3:
                fechas_disponibles.append({
                    'fecha': fecha.isoformat(),
                    'disponibles': 3 - count
                })
        
        cur.close()
        conn.close()
        return fechas_disponibles
    except Exception as e:
        print(f"Error en obtener_fechas_disponibles: {e}")
        return []


def obtener_citas_paciente(documento):
    """Obtener todas las citas de un paciente con información completa"""
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
                c.id            AS cita_id,
                c.tipo_cita,
                c.fecha,
                c.hora,
                c.direccion_eps,
                c.estado,
                m.nombre        AS medico,
                m.especialidad,
                p.nombre        AS pac_nombre,
                p.apellido      AS pac_apellido,
                p.eps
            FROM citas c
            INNER JOIN medicos m ON c.medico_id = m.id
            INNER JOIN pacientes p ON c.documento = p.documento
            WHERE c.documento = %s
            ORDER BY c.fecha DESC, c.hora DESC
        """, (documento,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_info_paciente(documento):
    """Obtener información del paciente"""
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT id, documento, nombre, apellido, telefono, correo, eps, created_at
            FROM pacientes
            WHERE documento = %s
        """, (documento,))
        return cur.fetchone()
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
                SUM(estado = 'Cancelada')                        AS canceladas,
                SUM(estado = 'Atendida')                         AS atendidas
            FROM citas
        """)
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def obtener_citas_por_medico(medico_id):
    """Citas asignadas a un médico (visibilidad por medico_id en citas)."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                c.id AS cita_id,
                c.documento,
                c.tipo_cita,
                c.fecha,
                c.hora,
                c.direccion_eps,
                c.estado,
                p.nombre AS pac_nombre,
                p.apellido AS pac_apellido,
                p.telefono,
                p.correo AS pac_correo,
                p.eps
            FROM citas c
            INNER JOIN pacientes p ON c.documento = p.documento
            WHERE c.medico_id = %s
            ORDER BY c.fecha DESC, c.hora DESC
            """,
            (medico_id,),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_cita_por_id_para_medico(cita_id, medico_id):
    """
    Una cita solo si pertenece al médico.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                c.*,
                p.nombre AS pac_nombre,
                p.apellido AS pac_apellido,
                p.telefono,
                p.correo AS pac_correo,
                p.eps,
                p.documento AS pac_documento,
                m.nombre AS medico_nombre, m.especialidad
            FROM citas c
            INNER JOIN pacientes p ON c.documento = p.documento
            INNER JOIN medicos m ON c.medico_id = m.id
            WHERE c.id = %s AND c.medico_id = %s
            """,
            (cita_id, medico_id),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def obtener_citas_paciente_para_medico(documento, medico_id):
    """
    Historial de citas del paciente con este médico (para el perfil médico).
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                c.id AS cita_id,
                c.tipo_cita,
                c.fecha,
                c.hora,
                c.estado,
                c.direccion_eps
            FROM citas c
            WHERE c.documento = %s AND c.medico_id = %s
            ORDER BY c.fecha DESC, c.hora DESC
            """,
            (documento, medico_id),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_historial_clinico_paciente_medico(documento, medico_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT h.id, h.notas, h.tipo, h.created_at,
                   c.fecha AS cita_fecha, c.id AS cita_id
            FROM historia_clinica h
            INNER JOIN citas c ON h.cita_id = c.id
            WHERE h.documento = %s AND h.medico_id = %s
            ORDER BY h.created_at DESC
            """,
            (documento, medico_id),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def obtener_pacientes_atendidos_por_medico(medico_id):
    """Pacientes con al menos una cita en estado Atendida con ese médico."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT DISTINCT p.documento, p.nombre, p.apellido, p.telefono, p.correo, p.eps
            FROM citas c
            INNER JOIN pacientes p ON c.documento = p.documento
            WHERE c.medico_id = %s AND c.estado = 'Atendida'
            ORDER BY p.apellido, p.nombre
            """,
            (medico_id,),
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def registrar_atencion_medica(cita_id, medico_id, documento, notas, tipo='Control'):
    """
    Marca la cita como Atendida e inserta registro en historia_clinica.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT id, estado FROM citas WHERE id = %s AND medico_id = %s AND documento = %s
            """,
            (cita_id, medico_id, documento),
        )
        row = cur.fetchone()
        if not row:
            return False, "Cita no encontrada o no corresponde a este médico."
        if row["estado"] == "Cancelada":
            return False, "No se puede atender una cita cancelada."
        if row["estado"] == "Atendida":
            return False, "Esta cita ya fue registrada como atendida."

        cur.execute(
            "UPDATE citas SET estado = 'Atendida' WHERE id = %s",
            (cita_id,),
        )
        cur.execute(
            """
            INSERT INTO historia_clinica (cita_id, medico_id, documento, notas, tipo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (cita_id, medico_id, documento, notas, tipo),
        )
        conn.commit()
        return True, "Atención registrada correctamente."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()
