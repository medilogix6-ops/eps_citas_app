# MEDILOGIX - Sistema de Gestión de Citas Médicas 2026

## 🏥 Descripción General

MEDILOGIX es una plataforma integral de gestión de citas médicas desarrollada para hospitales y centros de salud en Barranquilla, Colombia. La aplicación facilita la administración de citas, pacientes, médicos y usuarios del sistema.

### Información de la Empresa
- **Nombre**: MEDILOGIX
- **Ubicación**: Barranquilla, Colombia
- **Red**: Múltiples Hospitales Asociados
- **Año de Desarrollo**: 2026
- **Tecnología**: Python, Flask, MySQL

---

## 🚀 Nuevas Características 2026

### 1. Portal de Inicio
- Landing page profesional con información de MEDILOGIX
- Opciones claras de "Iniciar Sesión" y "Registrarse"
- Descripción de servicios y características
- Diseño responsivo y moderno

### 2. Registro Público
Los pacientes pueden registrarse directamente desde:
- **URL**: `/registro-portal`
- **Campos**: Usuario, Correo, Contraseña, Documento, Datos Personales
- Se crea automáticamente un usuario de tipo "Paciente"
- Se registra en la base de datos como paciente

### 3. Gestión Avanzada de Usuarios (Admin)
- Nueva opción: **"Crear Nuevo Usuario"** desde el Dashboard
- **URL**: `/usuarios/crear`
- El administrador puede crear usuarios de cualquier rol:
  - Paciente
  - Administrador
  - Médico
- Acceso rápido desde:
  - Dashboard (botón superior)
  - Página de Usuarios (botón superior)

### 4. Dashboard con Gráficos Interactivos
El nuevo dashboard administrativo incluye:

#### Visualizaciones:
- **Tarjetas de Estadísticas**: Total, Pendientes, Confirmadas, Canceladas
- **Gráfico de Barras**: Distribución de citas por estado
- **Chart.js**: Gráficos en tiempo real

#### Filtros:
- **Por Tipo de Cita**: General, Odontología, Especialista
- **Por Doctor**: Selecciona el médico (cuando implementes la carga dinámica)
- Los gráficos se actualizan automáticamente

#### API:
```
GET /api/estadisticas-filtradas?tipo_cita=General&medico_id=1
```

### 5. Navegación Reorganizada

**Sidebar para Administrador:**
- 📊 Dashboard
- 🧑‍⚕️ Pacientes
- 👤 Usuarios
- 👨‍⚕️ Médicos
- 🗓️ Todas las Citas

**Sidebar para Paciente:**
- 👤 Mi Perfil
- 📅 Reservar Cita

### 6. Branding MEDILOGIX
- Logo actualizado en todo el sistema
- Footer con información de la empresa
- Año 2026 en todas las referencias
- Colores y diseño profesionales

---

## 📋 Instrucciones de Uso

### Para Pacientes

#### 1. Registro
1. Ir al portal (`/`)
2. Clic en "📝 Registrarse"
3. Completar formulario:
   - Nombre de usuario
   - Correo electrónico
   - Contraseña (mín. 6 caracteres, mayúscula, número)
   - Documento de identidad
   - Datos personales
   - EPS
4. Iniciar sesión con las credenciales creadas

#### 2. Agendar Cita
1. Ir a "📅 Reservar Cita"
2. Seleccionar tipo de cita (General, Odontología, Especialista)
3. Elegir médico disponible
4. Seleccionar fecha
5. Confirmar reserva

#### 3. Ver Perfil
- Acceder a "👤 Mi Perfil"
- Ver historial de citas personales
- Estado de cada cita (Pendiente, Confirmada, Cancelada)

### Para Administradores

#### 1. Crear Nuevo Usuario
1. Ir a Dashboard
2. Clic en "➕ Nuevo Usuario" (botón superior)
3. Completar formulario:
   - Usuario
   - Correo
   - Contraseña
   - Rol (Paciente, Administrador, Médico)
4. El usuario se crea en la BD inmediatamente

#### 2. Ver Estadísticas
1. Dashboard principal
2. Gráfico de citas automáticamente visible
3. Usar filtros:
   - Tipo de cita
   - Doctor asignado

#### 3. Gestionar Pacientes
1. Clic en "🧑‍⚕️ Pacientes"
2. Ver lista con información
3. Registrar nuevo paciente
4. Editar paciente existente

#### 4. Gestionar Usuarios
1. Clic en "👤 Usuarios"
2. Ver todos los usuarios del sistema
3. Crear nuevo usuario
4. Editar usuario
5. Activar/Desactivar usuario

#### 5. Gestionar Médicos
1. Clic en "👨‍⚕️ Médicos"
2. Ver lista de médicos
3. Agregar nuevo médico
4. Eliminar médico

#### 6. Ver Todas las Citas
1. Clic en "🗓️ Todas las Citas"
2. Ver citas agendadas
3. Actualizar estado de cita
4. Cancelar cita si es necesario

---

## 🔐 Credenciales de Acceso (Demo)

| Tipo | Usuario | Contraseña |
|------|---------|-----------|
| Administrador | `admin` | `Admin2025*` |

---

## 📚 Archivos Principales

### Nuevos Archivos Creados:
- `templates/portal.html` - Portal de inicio
- `templates/registro_portal.html` - Registro público
- `templates/crear_usuario.html` - Crear usuarios (admin)

### Archivos Modificados:
- `app.py` - Nuevas rutas y endpoints
- `templates/base.html` - Navegación y branding
- `templates/dashboard.html` - Gráficos interactivos
- `templates/lista_usuarios.html` - Botón crear usuario
- `templates/login.html` - Branding MEDILOGIX

---

## 🔄 Flujo de Datos

```
Portal (/) 
  ├─→ Registrarse (/registro-portal)
  │    └─→ Crear Usuario + Paciente
  └─→ Iniciar Sesión (/login)
       ├─→ [Admin] → Dashboard (/dashboard)
       │            ├─→ Gráficos y Filtros
       │            ├─→ Crear Usuario (/usuarios/crear)
       │            ├─→ Gestionar Pacientes
       │            ├─→ Gestionar Médicos
       │            └─→ Ver Todas las Citas
       └─→ [Paciente] → Perfil (/perfil)
                      ├─→ Ver mis Citas
                      └─→ Reservar Nueva Cita (/citas/reservar)
```

---

## 📊 Tecnologías Utilizadas

- **Backend**: Python 3, Flask 3.0.3
- **Base de Datos**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js (CDN)
- **Autenticación**: bcrypt
- **Servidor**: Gunicorn

---

## ✅ Checklist de Funcionalidades

### Completadas:
- ✅ Portal profesional de inicio
- ✅ Registro público de pacientes
- ✅ Creación de usuarios desde admin
- ✅ Gráficos de citas médicas
- ✅ Filtros por tipo de cita y doctor
- ✅ Navegación mejorada
- ✅ Branding MEDILOGIX
- ✅ Año 2026 en todo el sistema
- ✅ Remover botón "Reservar Cita" del administrador
- ✅ Remover sección "Información del Sistema"
- ✅ Sidebar reorganizado

### Por Implementar (Sugerencias):
- 📋 Carga dinámica de médicos en filtros
- 📧 Sistema de notificaciones por correo
- 📱 App móvil
- 🔔 Recordatorios de citas
- 📊 Reportes más avanzados

---

## 🆘 Soporte y Contacto

**MEDILOGIX - Red de Salud Integral**
- 📍 Barranquilla, Colombia
- 📞 Atención 24/7 para pacientes
- 🏥 Múltiples sedes asociadas
- ✅ Acreditación ISO 9001:2015

---

## 📝 Notas de Desarrollo

- Contraseña demo del admin: `Admin2025*`
- Las fechas de demo están en 2026
- Chart.js se carga desde CDN para mejor rendimiento
- Los filtros del dashboard son en tiempo real
- La API `/api/estadisticas-filtradas` es extensible

---

**Última Actualización**: Marzo 2026  
**Versión**: 2.0 - MEDILOGIX Edition
