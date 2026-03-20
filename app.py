import os, sys
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
from models.citas     import (reservar_cita, consultar_citas_paciente,
                              obtener_todas_citas, obtener_cita_por_id,
                              actualizar_cita, eliminar_cita, estadisticas)

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

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
        if session.get('rol') != 'Administrador':
            flash('Acceso restringido a administradores.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return login_required(decorated)

# ──────────────────────────────────────────────
#  AUTH
# ──────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        # Admin va al Dashboard, Paciente va directamente a Reservar Cita
        if session.get('rol') == 'Administrador':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('reservar'))
    return redirect(url_for('login_view'))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = login(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['rol'] = user['rol']
            flash(f'Bienvenido, {user["username"]} 👋', 'success')
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login_view'))

# ──────────────────────────────────────────────
#  DASHBOARD
# ──────────────────────────────────────────────
@app.route('/dashboard')
@admin_required
def dashboard():
    stats = estadisticas()
    return render_template('dashboard.html', stats=stats)

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
    if nom and esp:
        ok, msg = agregar_medico(nom, esp)
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
    medicos = listar_medicos()
    if request.method == 'POST':
        doc   = request.form.get('documento','').strip()
        mid   = request.form.get('medico_id','').strip()
        tipo  = request.form.get('tipo_cita','').strip()
        fecha = request.form.get('fecha','').strip()
        hora  = request.form.get('hora','').strip()
        dir_  = request.form.get('direccion_eps','').strip()
        if not existe_paciente(doc):
            flash('No existe un paciente con ese documento. Regístrelo primero.', 'error')
        elif not all([mid, tipo, fecha, hora, dir_]):
            flash('Todos los campos son obligatorios.', 'error')
        else:
            ok, msg = reservar_cita(doc, mid, tipo, fecha, hora, dir_)
            flash(msg, 'success' if ok else 'error')
            if ok:
                return redirect(url_for('consulta_cita'))
    return render_template('reservar_cita.html', medicos=medicos)

@app.route('/citas/consulta', methods=['GET', 'POST'])
@login_required
def consulta_cita():
    citas     = []
    documento = ''
    if request.method == 'POST':
        documento = request.form.get('documento','').strip()
        citas     = consultar_citas_paciente(documento)
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
#  HEALTH CHECK
# ──────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
