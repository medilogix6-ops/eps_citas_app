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


def obtener_fechas_disponibles(medico_id, tipo_cita, dias=30):
    """Obtener fechas disponibles (máx 3 pacientes por día) para un médico"""
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    try:
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
        
        return fechas_disponibles
    finally:
        cur.close()
        conn.close()


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
                SUM(estado = 'Cancelada')                        AS canceladas
            FROM citas
        """)
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()
