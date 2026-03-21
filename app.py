import os, sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))

from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session, jsonify)
from functools import wraps
from config import Config
from database import init_db
from models.usuarios  import (
    login,
    registrar_usuario,
    listar_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    toggle_activo,
)
from models.pacientes import registrar_paciente, existe_paciente, obtener_todos, actualizar_paciente
from models.medicos   import listar_medicos, agregar_medico, eliminar_medico
from models.citas     import (reservar_cita, obtener_citas_paciente,
                              obtener_todas_citas, obtener_cita_por_id,
                              actualizar_cita, eliminar_cita, estadisticas,
                              obtener_medicos_por_tipo, obtener_fechas_disponibles,
                              obtener_info_paciente)

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Detectar si estamos en producción (Railway usa HTTPS)
IS_PRODUCTION = os.environ.get('RAILWAY_ENVIRONMENT') is not None or \
                os.environ.get('RAILWAY_PROJECT_ID') is not None

# Configurar sesiones — SECURE=True es obligatorio en HTTPS (Railway)
app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 horas

try:
    init_db()
    print("✅ Base de datos inicializada.")
except Exception as e:
    print(f"⚠️  DB init error: {e}")

# ──────────────────────────────────────────────
#  DECORADORES DE ACCESO
# ──────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión.', 'error')
            return redirect(url_for('login_view'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión.', 'error')
            return redirect(url_for('login_view'))
        
        if session.get('rol') != 'Administrador':
            flash('Acceso restringido a administradores.', 'error')
            # Redirige a un lugar seguro según el rol
            if session.get('rol') == 'Paciente':
                return redirect(url_for('perfil_paciente'))
            else:
                return redirect(url_for('portal'))
        
        return f(*args, **kwargs)
    return decorated

# ──────────────────────────────────────────────
#  PORTAL - INICIO
# ──────────────────────────────────────────────
@app.route('/')
def portal():
    if 'user_id' in session:
        if session.get('rol') == 'Administrador':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('perfil_paciente'))
    return render_template('portal.html')

# ──────────────────────────────────────────────
#  AUTH
# ──────────────────────────────────────────────
@app.route('/index')
def index():
    if 'user_id' in session:
        if session.get('rol') == 'Administrador':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('perfil_paciente'))
    return redirect(url_for('portal'))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if 'user_id' in session:
        if session.get('rol') == 'Administrador':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('perfil_paciente'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = login(username, password)
        
        if user:
            # Guardar datos en sesión
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['correo'] = user.get('correo', '')
            session['rol'] = user['rol']
            
            # Si es paciente, buscar su documento
            if user['rol'] == 'Paciente':
                from database import get_connection
                conn = get_connection()
                cur = conn.cursor(dictionary=True)
                try:
                    # Buscar paciente por correo
                    cur.execute(
                        "SELECT documento FROM pacientes WHERE correo = %s LIMIT 1",
                        (user.get('correo'),)
                    )
                    resultado = cur.fetchone()
                    if resultado:
                        session['documento_paciente'] = resultado['documento']
                finally:
                    cur.close()
                    conn.close()
            
            flash(f'Bienvenido, {user["username"]} 👋', 'success')
            
            # Redirigir según el rol
            if user['rol'] == 'Administrador':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('perfil_paciente'))
        
        flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

@app.route('/registro-portal', methods=['GET', 'POST'])
def registro_portal():
    """Registro de nuevos pacientes desde el portal público"""
    if 'user_id' in session:
        if session.get('rol') == 'Administrador':
            return redirect(url_for('dashboard'))
        return redirect(url_for('perfil_paciente'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '').strip()
        documento = request.form.get('documento', '').strip()
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        telefono = request.form.get('telefono', '').strip()
        eps = request.form.get('eps', '').strip()
        
        # Validar datos
        if not all([username, correo, password, documento, nombre, apellido, telefono, eps]):
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('registro_portal.html')
        
        # Registrar usuario (rol_id=2 es Paciente)
        ok_user, msg_user = registrar_usuario(username, correo, password, rol_id=2)
        
        if not ok_user:
            flash(f'Error al registrar usuario: {msg_user}', 'error')
            return render_template('registro_portal.html')
        
        # Registrar paciente
        ok_paciente, msg_paciente = registrar_paciente(documento, nombre, apellido, telefono, correo, eps)
        
        if ok_paciente:
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login_view'))
        else:
            flash(f'Usuario creado pero error al registrar paciente: {msg_paciente}', 'warning')
            return redirect(url_for('login_view'))
    
    return render_template('registro_portal.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('portal'))

# ──────────────────────────────────────────────
#  PERFIL DEL PACIENTE
# ──────────────────────────────────────────────
@app.route('/perfil')
@login_required
def perfil_paciente():
    """Perfil del paciente con su información y citas"""
    # Si es administrador, no puede acceder
    if session.get('rol') == 'Administrador':
        flash('Esta página es solo para pacientes.', 'error')
        return redirect(url_for('dashboard'))
    
    # Obtener documento del paciente
    doc = session.get('documento_paciente')
    
    # Si no está en sesión, intentar obtenerlo de la BD
    if not doc:
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT documento FROM pacientes WHERE correo = %s LIMIT 1",
                (session.get('correo'),)
            )
            resultado = cur.fetchone()
            if resultado:
                doc = resultado['documento']
                session['documento_paciente'] = doc
        finally:
            cur.close()
            conn.close()
    
    # Si aún no tiene documento, mostrar perfil vacío con mensaje
    if not doc:
        flash('No se encontró tu información de paciente. Si te registraste recientemente, '
              'contacta al administrador.', 'warning')
        return render_template('perfil_paciente.html', paciente=None, citas=[])
    
    # Obtener información del paciente
    paciente = obtener_info_paciente(doc)
    
    if not paciente:
        flash('Paciente no encontrado en el sistema. Contacta al administrador.', 'error')
        return render_template('perfil_paciente.html', paciente=None, citas=[])
    
    # Obtener citas del paciente
    citas = obtener_citas_paciente(doc) if paciente else []
    
    return render_template('perfil_paciente.html', paciente=paciente, citas=citas)

# ──────────────────────────────────────────────
#  API ENDPOINTS (para AJAX)
# ──────────────────────────────────────────────
@app.route('/api/medicos-por-tipo/<tipo_cita>')
@login_required
def api_medicos_por_tipo(tipo_cita):
    """Obtener médicos disponibles para un tipo de cita"""
    try:
        medicos = obtener_medicos_por_tipo(tipo_cita)
        return jsonify([dict(m) if hasattr(m, 'keys') else m for m in (medicos or [])])
    except Exception as e:
        print(f"Error en api_medicos_por_tipo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/fechas-disponibles/<int:medico_id>')
@login_required
def api_fechas_disponibles(medico_id):
    """Obtener fechas disponibles para un médico (máx 3 pacientes por día)"""
    try:
        fechas = obtener_fechas_disponibles(medico_id)
        return jsonify({'fechas': fechas or []})
    except Exception as e:
        print(f"Error en api_fechas_disponibles: {e}")
        return jsonify({'error': str(e), 'fechas': []}), 500

# ──────────────────────────────────────────────
#  DASHBOARD
# ──────────────────────────────────────────────
@app.route('/dashboard')
@admin_required
def dashboard():
    stats = estadisticas()
    return render_template('dashboard.html', stats=stats)

@app.route('/api/estadisticas-filtradas')
@admin_required
def api_estadisticas_filtradas():
    """API para obtener estadísticas filtradas por tipo de cita y doctor"""
    from database import get_connection
    
    tipo_cita = request.args.get('tipo_cita', '')  # General, Odontología, Especialista
    medico_id = request.args.get('medico_id', '')   # ID del médico
    
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        # Query base
        query = "SELECT estado, COUNT(*) as count FROM citas WHERE 1=1"
        params = []
        
        if tipo_cita:
            query += " AND tipo_cita = %s"
            params.append(tipo_cita)
        
        if medico_id:
            query += " AND medico_id = %s"
            params.append(medico_id)
        
        query += " GROUP BY estado"
        
        cur.execute(query, params)
        resultados = cur.fetchall()
        
        # Crear diccionario con estados como claves
        stats = {
            'Pendiente': 0,
            'Confirmada': 0,
            'Cancelada': 0
        }
        
        for row in resultados:
            stats[row['estado']] = row['count']
        
        return jsonify(stats)
    except Exception as e:
        print(f"Error en api_estadisticas_filtradas: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ──────────────────────────────────────────────
#  PACIENTES
# ──────────────────────────────────────────────
@app.route('/pacientes')
@admin_required
def lista_pacientes():
    pacientes = obtener_todos()
    return render_template('lista_pacientes.html', pacientes=pacientes)

@app.route('/pacientes/registro', methods=['GET', 'POST'])
@admin_required
def registro_paciente():
    if request.method == 'POST':
        doc  = request.form.get('documento','').strip()
        nom  = request.form.get('nombre','').strip()
        ape  = request.form.get('apellido','').strip()
        tel  = request.form.get('telefono','').strip()
        cor  = request.form.get('correo','').strip()
        eps  = request.form.get('eps','').strip()
        if not all([doc, nom, ape]):
            flash('Documento, nombre y apellido son obligatorios.', 'error')
        else:
            ok, msg = registrar_paciente(doc, nom, ape, tel, cor, eps)
            flash(msg, 'success' if ok else 'error')
            if ok:
                return redirect(url_for('lista_pacientes'))
    return render_template('registro_paciente.html')

@app.route('/pacientes/editar/<documento>', methods=['GET', 'POST'])
@admin_required
def editar_paciente(documento):
    pac = existe_paciente(documento)
    if not pac:
        flash('Paciente no encontrado.', 'error')
        return redirect(url_for('lista_pacientes'))
    if request.method == 'POST':
        ok, msg = actualizar_paciente(
            documento,
            request.form.get('nombre','').strip(),
            request.form.get('apellido','').strip(),
            request.form.get('telefono','').strip(),
            request.form.get('correo','').strip(),
            request.form.get('eps','').strip(),
        )
        flash(msg, 'success' if ok else 'error')
        if ok:
            return redirect(url_for('lista_pacientes'))
    return render_template('editar_paciente.html', pac=pac)

# ──────────────────────────────────────────────
#  MÉDICOS  (solo admin)
# ──────────────────────────────────────────────
@app.route('/medicos')
@admin_required
def lista_medicos():
    medicos = listar_medicos()
    return render_template('lista_medicos.html', medicos=medicos)

@app.route('/medicos/agregar', methods=['POST'])
@admin_required
def agregar_medico_view():
    nom  = request.form.get('nombre','').strip()
    esp  = request.form.get('especialidad','').strip()
    dir  = request.form.get('direccion','').strip()
    if nom and esp:
        ok, msg = agregar_medico(nom, esp, dir)
        flash(msg, 'success' if ok else 'error')
    else:
        flash('Nombre y especialidad son obligatorios.', 'error')
    return redirect(url_for('lista_medicos'))

@app.route('/medicos/eliminar/<int:mid>', methods=['POST'])
@admin_required
def eliminar_medico_view(mid):
    ok, msg = eliminar_medico(mid)
    flash(msg, 'success' if ok else 'error')
    return redirect(url_for('lista_medicos'))

# ──────────────────────────────────────────────
#  CITAS
# ──────────────────────────────────────────────
@app.route('/citas')
@admin_required
def todas_citas():
    citas = obtener_todas_citas()
    return render_template('todas_citas.html', citas=citas)

@app.route('/citas/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    pac_doc = session.get('documento_paciente')
    
    if request.method == 'POST':
        mid   = request.form.get('medico_id','').strip()
        tipo  = request.form.get('tipo_cita','').strip()
        fecha = request.form.get('fecha','').strip()
        
        if not all([mid, tipo, fecha, pac_doc]):
            flash('Faltan datos requeridos.', 'error')
        else:
            ok, msg = reservar_cita(pac_doc, mid, tipo, fecha)
            flash(msg, 'success' if ok else 'error')
            if ok:
                return redirect(url_for('perfil_paciente'))
    
    return render_template('reservar_cita.html')

@app.route('/citas/consulta', methods=['GET', 'POST'])
@login_required
def consulta_cita():
    citas     = []
    documento = ''
    if request.method == 'POST':
        documento = request.form.get('documento','').strip()
        citas     = obtener_citas_paciente(documento)
        if not citas:
            flash('No se encontraron citas para ese documento.', 'error')
    return render_template('consulta_cita.html', citas=citas, documento=documento)

@app.route('/citas/actualizar/<int:cita_id>', methods=['GET', 'POST'])
@login_required
def actualizar(cita_id):
    cita    = obtener_cita_por_id(cita_id)
    medicos = listar_medicos()
    if not cita:
        flash('Cita no encontrada.', 'error')
        return redirect(url_for('consulta_cita'))
    if request.method == 'POST':
        ok, msg = actualizar_cita(
            cita_id,
            request.form.get('medico_id',''),
            request.form.get('tipo_cita',''),
            request.form.get('fecha',''),
            request.form.get('hora',''),
            request.form.get('direccion_eps',''),
            request.form.get('estado','Pendiente'),
        )
        flash(msg, 'success' if ok else 'error')
        if ok:
            return redirect(url_for('consulta_cita'))
    return render_template('actualizar_cita.html', cita=cita, medicos=medicos)

@app.route('/citas/eliminar/<int:cita_id>', methods=['POST'])
@login_required
def eliminar(cita_id):
    ok, msg = eliminar_cita(cita_id)
    flash(msg, 'success' if ok else 'error')
    return redirect(url_for('consulta_cita'))

# ──────────────────────────────────────────────
#  USUARIOS  (solo admin)
# ──────────────────────────────────────────────
@app.route('/usuarios')
@admin_required
def lista_usuarios():
    usuarios = listar_usuarios()
    return render_template('lista_usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
@admin_required
def crear_usuario():
    """Crear nuevo usuario desde el admin"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '').strip()
        rol_id = int(request.form.get('rol_id', 2))
        
        if not all([username, correo, password]):
            flash('Usuario, correo y contraseña son obligatorios.', 'error')
        else:
            ok, msg = registrar_usuario(username, correo, password, rol_id)
            flash(msg, 'success' if ok else 'error')
            if ok:
                return redirect(url_for('lista_usuarios'))
    
    return render_template('crear_usuario.html')

@app.route('/usuarios/editar/<int:uid>', methods=['GET', 'POST'])
@admin_required
def editar_usuario(uid):
    user = obtener_usuario_por_id(uid)
    if not user:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('lista_usuarios'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        correo   = request.form.get('correo', '').strip()
        rol_id   = int(request.form.get('rol_id', user['rol_id']))
        password = request.form.get('password', '').strip()

        if not username or not correo:
            flash('Usuario y correo son obligatorios.', 'error')
        else:
            ok, msg = actualizar_usuario(uid, username, correo, rol_id, password or None)
            flash(msg, 'success' if ok else 'error')
            if ok:
                return redirect(url_for('lista_usuarios'))

    return render_template('editar_usuario.html', user=user)


@app.route('/usuarios/toggle/<int:uid>', methods=['POST'])
@admin_required
def toggle_usuario(uid):
    toggle_activo(uid)
    flash('Estado del usuario actualizado.', 'success')
    return redirect(url_for('lista_usuarios'))

# ──────────────────────────────────────────────
#  SESIONES Y CACHÉ
# ──────────────────────────────────────────────
@app.before_request
def before_request():
    """Marcar sesión como permanente"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=24)

# ──────────────────────────────────────────────
#  HEALTH CHECK
# ──────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
