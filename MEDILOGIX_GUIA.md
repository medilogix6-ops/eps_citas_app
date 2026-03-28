# MEDILOGIX - Sistema de Gestión de Citas Médicas 2026

## 🏥 Descripción General

MEDILOGIX es una plataforma integral de gestión de citas médicas desarrollada para hospitales y centros de salud en Barranquilla, Colombia. La aplicación web facilita la administración completa de citas, pacientes, médicos y usuarios del sistema a través de una interfaz intuitiva y moderna.

### Información de la Empresa
- **Nombre**: MEDILOGIX
- **Ubicación**: Barranquilla, Colombia
- **Red**: Múltiples Hospitales Asociados
- **Año de Desarrollo**: 2026
- **Tecnología**: Python, Flask, MySQL
- **Tipo de Aplicación**: Web App (Flask Framework)
- **Despliegue**: Railway (web-production-6f3f2.up.railway.app)
- **Repositorio**: [GitHub](https://github.com/medilogix6-ops/eps_citas_app.git)

---

## 🚀 Características Principales de la Aplicación Web

### 1. Portal de Inicio Profesional
- **Página de destino** (`/`) con diseño moderno y responsivo
- Información corporativa de MEDILOGIX
- Botones claros para "Iniciar Sesión" y "Registrarse"
- Descripción de servicios médicos disponibles
- Navegación intuitiva hacia el registro público

### 2. Sistema de Registro Público
Los pacientes pueden registrarse directamente desde la web:
- **URL de acceso**: `/registro-portal`
- **Formulario web interactivo** con validación en tiempo real
- **Campos requeridos**:
  - Nombre de usuario único
  - Correo electrónico válido
  - Contraseña segura (mín. 6 caracteres, mayúscula, número)
  - Documento de identidad
  - Datos personales completos (nombre, apellido, teléfono, EPS)
- **Creación automática**: Usuario de tipo "Paciente" + registro en base de datos
- **Confirmación inmediata**: Acceso directo al sistema tras registro

### 3. Gestión Avanzada de Usuarios (Panel Administrativo)
- **Nueva funcionalidad**: "Crear Nuevo Usuario" desde el dashboard web
- **URL**: `/usuarios/crear`
- **Permisos administrativos**: Crear usuarios de cualquier rol (Paciente, Administrador, Médico)
- **Acceso rápido**: Botones en dashboard y página de usuarios
- **Interfaz web**: Formularios dinámicos con validación

### 4. Dashboard Interactivo con Visualizaciones Web
El dashboard administrativo incluye gráficos y estadísticas en tiempo real:

#### Elementos Visuales:
- **Tarjetas de métricas**: Total de citas, Pendientes, Confirmadas, Canceladas
- **Gráfico de barras interactivo**: Distribución por estado de citas (usando Chart.js)
- **Actualización automática**: Datos en tiempo real sin recargar página

#### Filtros Dinámicos:
- **Por tipo de cita**: General, Odontología, Especialista
- **Por médico**: Selector desplegable (preparado para carga dinámica)
- **API integrada**: `/api/estadisticas-filtradas?tipo_cita=General&medico_id=1`
- **Interfaz web**: Filtros aplicados con JavaScript para actualización instantánea

### 5. Navegación Web Reorganizada

**Panel Lateral para Administrador:**
- 📊 Dashboard (con gráficos)
- 🧑‍⚕️ Gestión de Pacientes
- 👤 Gestión de Usuarios
- 👨‍⚕️ Gestión de Médicos
- 🗓️ Todas las Citas

**Panel Lateral para Paciente:**
- 👤 Mi Perfil Personal
- 📅 Reservar Nueva Cita

### 6. Branding y Diseño Web MEDILOGIX
- **Logo corporativo** en todas las páginas
- **Footer informativo** con datos de la empresa
- **Año 2026** en referencias y copyrights
- **Paleta de colores** profesional y accesible
- **Diseño responsivo**: Compatible con móviles y tablets

### 7. Sistema de Autenticación Web Seguro
- **Login centralizado** (`/login`) con validación
- **Sesiones seguras** usando Flask-Login
- **Encriptación de contraseñas** con bcrypt
- **Roles y permisos**: Diferentes vistas según el tipo de usuario

### 8. Gestión Completa de Citas Web
- **Reserva online**: Pacientes pueden agendar citas desde la web
- **Estados de citas**: Pendiente, Confirmada, Cancelada, Atendida
- **Vista médica**: Médicos pueden atender y gestionar citas
- **Historial completo**: Seguimiento de todas las citas del sistema

### 9. Módulos de Gestión Web
- **Pacientes**: Registro, edición, listado con búsqueda
- **Médicos**: CRUD completo con especialidades
- **Usuarios**: Gestión de roles y permisos
- **Citas**: Vista unificada de todas las citas del sistema

---

## 📋 Guía de Uso de la Aplicación Web

### Para Pacientes (Acceso Web)

#### 1. Registro Inicial
1. Acceder al portal principal: `https://web-production-6f3f2.up.railway.app/`
2. Hacer clic en "📝 Registrarse"
3. Completar el formulario web:
   - Usuario único
   - Email válido
   - Contraseña segura
   - Documento de identidad
   - Información personal y EPS
4. Confirmar registro y acceder automáticamente

#### 2. Reservar Cita Médica
1. Desde el panel lateral: "📅 Reservar Cita"
2. Seleccionar tipo de cita (General, Odontología, Especialista)
3. Elegir médico disponible del listado
4. Seleccionar fecha disponible (calendario web)
5. Confirmar la reserva (notificación inmediata)

#### 3. Gestionar Mi Perfil
- Acceder a "👤 Mi Perfil"
- Ver historial completo de citas personales
- Estados actualizados: Pendiente, Confirmada, Cancelada, Atendida
- Información personal editable

### Para Administradores (Panel Web Completo)

#### 1. Crear Nuevos Usuarios
1. Desde Dashboard: botón "➕ Nuevo Usuario"
2. Formulario web para crear usuarios de cualquier rol
3. Campos: Usuario, Email, Contraseña, Rol asignado
4. Creación inmediata en base de datos

#### 2. Analizar Estadísticas
1. Dashboard principal con métricas visuales
2. Gráficos de barras interactivos (Chart.js)
3. Filtros en tiempo real:
   - Tipo de cita
   - Médico específico
4. Exportación de datos vía API

#### 3. Gestionar Pacientes
1. Módulo "🧑‍⚕️ Pacientes"
2. Listado con búsqueda y filtros
3. Registrar nuevos pacientes
4. Editar información existente
5. Ver historial de citas por paciente

#### 4. Gestionar Usuarios del Sistema
1. Módulo "👤 Usuarios"
2. Vista completa de todos los usuarios
3. Crear, editar, activar/desactivar usuarios
4. Gestión de roles y permisos

#### 5. Gestionar Médicos
1. Módulo "👨‍⚕️ Médicos"
2. CRUD completo de profesionales
3. Asignación de especialidades
4. Control de disponibilidad

#### 6. Supervisar Todas las Citas
1. Módulo "🗓️ Todas las Citas"
2. Vista unificada del sistema
3. Actualizar estados de citas
4. Cancelar o reprogramar cuando sea necesario

---

## 🔐 Credenciales de Acceso (Demo)

| Tipo | Usuario | Contraseña | URL de Acceso |
|------|---------|-----------|---------------|
| Administrador | `admin` | `Admin2025*` | [web-production-6f3f2.up.railway.app/login](https://web-production-6f3f2.up.railway.app/login) |

---

## 📚 Arquitectura Técnica de la Web App

### Backend (Flask Python)
- **Framework**: Flask 3.0.3
- **Base de Datos**: MySQL 8.0+
- **Autenticación**: Flask-Login + bcrypt
- **APIs REST**: Endpoints para estadísticas y datos
- **Sesiones**: Gestión segura de usuarios

### Frontend (HTML/CSS/JS)
- **Templates**: Jinja2 (Flask)
- **Estilos**: CSS3 personalizado + Bootstrap
- **Gráficos**: Chart.js (CDN)
- **Interactividad**: JavaScript vanilla
- **Responsivo**: Diseño mobile-first

### Base de Datos
- **Motor**: MySQL
- **Tablas principales**: usuarios, pacientes, medicos, citas
- **Relaciones**: Claves foráneas para integridad
- **Migraciones**: Script SQL incluido

### Despliegue
- **Plataforma**: Railway
- **URL de Producción**: https://web-production-6f3f2.up.railway.app
- **Configuración**: Procfile para Gunicorn
- **Variables de entorno**: Configuración segura

---

## 📁 Estructura de Archivos de la Web App

### Archivos Principales:
- `app.py` - Aplicación Flask principal con todas las rutas
- `config.py` - Configuración de base de datos y app
- `database.py` - Conexiones y operaciones de BD
- `requirements.txt` - Dependencias Python
- `Procfile` - Configuración para despliegue

### Modelos (models/):
- `usuarios.py` - Gestión de usuarios y autenticación
- `pacientes.py` - Datos de pacientes
- `medicos.py` - Información de médicos
- `citas.py` - Sistema de citas médicas

### Templates Web (templates/):
- `portal.html` - Página de inicio pública
- `registro_portal.html` - Formulario de registro público
- `login.html` - Página de autenticación
- `dashboard.html` - Panel administrativo con gráficos
- `base.html` - Plantilla base con navegación
- `crear_usuario.html` - Formulario creación de usuarios

### Estilos (static/css/):
- `style.css` - Estilos personalizados MEDILOGIX

---

## 🔄 Flujo de Navegación Web

```
Portal Público (/)
├── Registrarse (/registro-portal)
│   └── Crear Usuario + Paciente → Login
└── Iniciar Sesión (/login)
    ├── [Admin] Dashboard (/dashboard)
    │   ├── Gráficos Interactivos
    │   ├── Crear Usuario (/usuarios/crear)
    │   ├── Gestionar Pacientes (/pacientes)
    │   ├── Gestionar Médicos (/medicos)
    │   └── Ver Todas las Citas (/citas/todas)
    └── [Paciente] Perfil (/perfil)
        ├── Ver Mis Citas
        └── Reservar Cita (/citas/reservar)
```

---

## 📊 Tecnologías Web Utilizadas

- **Backend Web**: Python 3.x, Flask 3.0.3
- **Base de Datos**: MySQL 8.0+
- **Frontend Web**: HTML5, CSS3, JavaScript ES6
- **Gráficos**: Chart.js 4.x (CDN)
- **Autenticación**: Flask-Login, bcrypt
- **Servidor Web**: Gunicorn
- **Despliegue**: Railway
- **Control de Versiones**: Git (GitHub)

---

## ✅ Funcionalidades Web Implementadas

### ✅ Completadas:
- ✅ Portal web profesional de inicio
- ✅ Sistema de registro público web
- ✅ Creación de usuarios desde panel admin
- ✅ Dashboard con gráficos interactivos web
- ✅ Filtros dinámicos en tiempo real
- ✅ Navegación web reorganizada por roles
- ✅ Branding MEDILOGIX completo
- ✅ Autenticación web segura
- ✅ Gestión completa de citas web
- ✅ Módulos CRUD para pacientes, médicos, usuarios
- ✅ Diseño responsivo para móviles
- ✅ API REST para estadísticas
- ✅ Despliegue en producción (Railway)

### 🔄 En Desarrollo:
- 📋 Carga dinámica de médicos en filtros
- 📧 Sistema de notificaciones por email
- 📱 Optimización para dispositivos móviles
- 🔔 Recordatorios automáticos de citas
- 📊 Reportes avanzados exportables

---

## 🌐 Enlaces Importantes

- **Aplicación Web Desplegada**: [https://web-production-6f3f2.up.railway.app](https://web-production-6f3f2.up.railway.app)
- **Repositorio GitHub**: [https://github.com/medilogix6-ops/eps_citas_app.git](https://github.com/medilogix6-ops/eps_citas_app.git)
- **Documentación**: Este archivo (MEDILOGIX_GUIA.md)

---

## 🆘 Soporte y Contacto

**MEDILOGIX - Red de Salud Integral**
- 📍 Barranquilla, Colombia
- 📞 Atención 24/7 para pacientes
- 🏥 Múltiples sedes asociadas
- ✅ Acreditación ISO 9001:2015
- 🌐 Web: https://web-production-6f3f2.up.railway.app

---

## 📝 Notas Técnicas de Desarrollo

- **Contraseña demo admin**: `Admin2025*`
- **Fechas de demo**: Configuradas para 2026
- **Chart.js**: Carga desde CDN para rendimiento óptimo
- **Filtros dashboard**: Actualización AJAX en tiempo real
- **API extensible**: `/api/estadisticas-filtradas` preparada para expansiones
- **Base de datos**: Incluye script de creación completo
- **Despliegue**: Configurado para Railway con variables de entorno

---

**Última Actualización**: Marzo 2026  
**Versión**: 2.0 - MEDILOGIX Web Edition  
**Desarrollado por**: Equipo MEDILOGIX
