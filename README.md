# 🏥 EPS Citas Médicas — Sistema de Gestión

Aplicación web desarrollada en **Python + Flask + MySQL** para gestionar citas médicas.  
Proyecto académico — Programa ADSO19, SENA.

---

## 📁 Estructura del Proyecto

```
eps_citas_app/
├── app.py                      ← Aplicación Flask (rutas y lógica)
├── config.py                   ← Variables de entorno / configuración
├── database.py                 ← Conexión MySQL + inicialización de tablas
├── eps_citas_database.sql      ← Script SQL completo (referencia)
├── Procfile                    ← Comando de arranque para Railway
├── requirements.txt            ← Dependencias Python
├── .env.example                ← Plantilla de variables de entorno
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── usuarios.py             ← Login, registro, toggle activo
│   ├── pacientes.py            ← CRUD pacientes
│   ├── medicos.py              ← CRUD médicos
│   └── citas.py                ← CRUD citas + estadísticas
│
├── templates/
│   ├── base.html               ← Layout con sidebar (todas las páginas)
│   ├── login.html              ← Página de inicio de sesión
│   ├── dashboard.html          ← Panel principal con estadísticas
│   ├── registro_paciente.html  ← Formulario nuevo paciente
│   ├── editar_paciente.html    ← Editar datos de paciente
│   ├── lista_pacientes.html    ← Tabla de todos los pacientes
│   ├── reservar_cita.html      ← Formulario reserva de cita
│   ├── consulta_cita.html      ← Buscar citas por documento
│   ├── actualizar_cita.html    ← Editar cita existente
│   ├── todas_citas.html        ← Vista admin: todas las citas
│   ├── lista_medicos.html      ← Gestión de médicos (admin)
│   └── lista_usuarios.html     ← Gestión de usuarios (admin)
│
└── static/
    └── css/
        └── style.css           ← Diseño completo (sin dependencias externas excepto Google Fonts)
```

---

## 🚀 Despliegue en Railway (paso a paso)

### 1. Subir a GitHub

```bash
cd eps_citas_app
git init
git add .
git commit -m "feat: sistema de citas médicas EPS"
git remote add origin https://github.com/TU_USUARIO/eps-citas.git
git push -u origin main
```

### 2. Crear proyecto en Railway

1. Ir a [railway.app](https://railway.app) → **New Project**
2. Seleccionar **Deploy from GitHub repo** → elegir el repositorio
3. Agregar base de datos: botón **"+ New"** → **Database** → **MySQL**

### 3. Configurar Variables de Entorno

En el servicio Flask → pestaña **Variables**, agregar:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | (cualquier cadena larga y aleatoria) |

> Las variables `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DATABASE` las inyecta Railway automáticamente desde el plugin MySQL.

### 4. Deploy

Railway detecta el `Procfile` y lanza:
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
```
Las tablas y datos de prueba se crean **automáticamente** en el primer arranque.

---

## 💻 Desarrollo Local

```bash
# 1. Clonar / descomprimir el proyecto
cd eps_citas_app

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales MySQL locales

# 5. Importar la base de datos (opcional, la app lo hace automáticamente)
mysql -u root -p < eps_citas_database.sql

# 6. Ejecutar
python app.py
# → http://localhost:5000
```

---

## 🔐 Credenciales de Prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin` | `Admin2025*` |
| Paciente | `juan.perez` | `Paciente123*` |
| Paciente | `jorge` | `Paciente123` |
| Medico | `Andres` | `12345` |
| Medico | `juan` | `12345` |

---

## 🗄️ Modelo de Base de Datos

```
roles ──< usuarios
pacientes ──< citas >── medicos
```

**Tablas:** `roles`, `usuarios`, `pacientes`, `medicos`, `citas`

---

## ✅ Funcionalidades Implementadas

- [x] Login con autenticación bcrypt y roles (Admin / Paciente)
- [x] Dashboard con estadísticas de citas
- [x] CRUD completo de pacientes
- [x] CRUD completo de citas (con JOIN paciente + médico)
- [x] Gestión de médicos (solo Admin)
- [x] Gestión de usuarios — activar/desactivar (solo Admin)
- [x] Consulta de citas por número de documento
- [x] Estados de cita: Pendiente / Confirmada / Cancelada
- [x] Datos de prueba precargados automáticamente
- [x] Listo para Railway (Procfile + variables de entorno)
