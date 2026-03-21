# 🎬 GUÍA VISUAL - MEDILOGIX 2026

## 🚀 INICIO RÁPIDO

### Paso 1: Iniciar la Aplicación
```bash
cd c:\Users\Pequi\eps_citas_app
python app.py
```

Abre en el navegador:
```
http://localhost:5000/
```

---

## 📺 FLUJO DE USO POR TIPO DE USUARIO

### 👥 PACIENTE NUEVO

```
1. ACCESO AL PORTAL
   ┌─────────────────────────────────────┐
   │  🏥 MEDILOGIX                       │
   │  Red de Salud Integral              │
   │                                     │
   │  [🔐 Iniciar Sesión] [📝 REGISTRARSE]  
   └─────────────────────────────────────┘

2. HACER CLIC EN "📝 REGISTRARSE"
   ┌─────────────────────────────────────┐
   │  REGISTRO - MEDILOGIX               │
   │  👤 Datos de Usuario:               │
   │     Usuario: [____________]         │
   │     Correo: [____________]          │
   │     Contraseña: [________]          │
   │     Confirmar: [________]           │
   │                                     │
   │  📋 Datos Personales:               │
   │     Documento: [____________]       │
   │     Nombre: [____________]          │
   │     Apellido: [____________]        │
   │     Teléfono: [____________]        │
   │     EPS: [Seleccionar ▼]           │
   │                                     │
   │  [← ATRÁS] [✅ REGISTRARSE]        │
   └─────────────────────────────────────┘

3. COMPLETAR Y ENVIAR
   ✅ Usuario creado automáticamente
   ✅ Paciente registrado en BD
   ✅ Redirige a login

4. INICIAR SESIÓN
   ┌─────────────────────────────────────┐
   │  MEDILOGIX                          │
   │  Red de Salud Integral              │
   │                                     │
   │  Usuario: [usuario123          ]    │
   │  Contraseña: [••••••••         ]    │
   │                                     │
   │  [🔐 Iniciar Sesión]               │
   └─────────────────────────────────────┘

5. VER PERFIL Y AGENDAR CITA
   ┌─────────────────────────────────────┐
   │  SIDEBAR          │  CONTENIDO      │
   │  ┌───────────┐    │ ┌───────────┐  │
   │  │📊 Dash   │    │ │👤 MI PERFIL   │
   │  │           │    │ │               │
   │  │👤 MI     │    │ │Nombre: Juan   │
   │  │PERFIL    │    │ │Documento: ... │
   │  │           │    │ │EPS: Sanitas   │
   │  │📅 RESERVAR│    │ │               │
   │  │CITA      │    │ │📅 MIS CITAS:  │
   │  │           │    │ │ - Cita 1      │
   │  │🚪 CERRAR │    │ │   Estado: ... │
   │  └───────────┘    │ └───────────┘  │
   └─────────────────────────────────────┘

6. AGENDAR NUEVA CITA
   Clic en "📅 RESERVAR CITA"
   ┌─────────────────────────────────────┐
   │  RESERVAR CITA                      │
   │  Tipo: [General ▼]                 │
   │  Médico: [Seleccionar ▼]           │
   │  Fecha: [2026-07-15]               │
   │  [📅 Reservar]                     │
   └─────────────────────────────────────┘
   ✅ Cita creada
   ✅ Confirmación en perfil
```

---

### 👑 ADMINISTRADOR

```
1. INICIAR SESIÓN
   Usuario: admin
   Contraseña: Admin2025*

2. ACCEDER DASHBOARD
   ┌──────────────────────────────────────────────┐
   │  DASHBOARD MEDILOGIX                         │
   │  ┌────────────────────────────────────────┐  │
   │  │ Total: 5 │ Pendientes: 2 │ Confirmadas: 3 │
   │  └────────────────────────────────────────┘  │
   │                                              │
   │  ┌──────────────────────────────────────┐   │
   │  │  📊 ESTADÍSTICAS DE CITAS            │   │
   │  │                                      │   │
   │  │  Filtro: [General ▼] [Doctor ▼]   │   │
   │  │                                      │   │
   │  │  ┌──────────────────────────────┐  │   │
   │  │  │  Gráfico de Barras           │  │   │
   │  │  │  ▁▂▃ Citas en Tiempo Real   │  │   │
   │  │  └──────────────────────────────┘  │   │
   │  │                                      │   │
   │  │  Pendiente: 2 | Confirmada: 3      │   │
   │  └──────────────────────────────────┘   │
   │                                          │
   │  ⚡ ACCIONES RÁPIDAS:                   │
   │  [👤 Gestionar Usuarios]                │
   │  [🧑‍⚕️ Gestionar Pacientes]              │
   │  [👨‍⚕️ Gestionar Médicos]                │
   │  [🗓️ Ver Todas las Citas]              │
   └──────────────────────────────────────────────┘

3. USAR FILTROS
   - Selecciona "Tipo de Cita": General, Odontología, Especialista
   - El gráfico se actualiza automáticamente ✨
   - Selecciona "Doctor": médico específico
   - Los números se actualizan en tiempo real 📊

4. CREAR NUEVO USUARIO
   Botón: "➕ Nuevo Usuario" (esquina superior)
   ┌──────────────────────────────────────┐
   │  ➕ CREAR NUEVO USUARIO             │
   │  Usuario: [____________]             │
   │  Correo: [________________]          │
   │  Contraseña: [__________]            │
   │  Rol: [Paciente ▼]                 │
   │       [Administrador]               │
   │       [Médico]                      │
   │  [← ATRÁS] [✅ CREAR USUARIO]       │
   └──────────────────────────────────────┘
   ✅ Usuario guardado en BD
   ✅ Vuelve a lista de usuarios

5. GESTIONAR PACIENTES
   Sidebar → "🧑‍⚕️ Pacientes"
   ┌──────────────────────────────────────────┐
   │  Pacientes Registrados (3)               │
   │  ┌──────────────────────────────────────┐│
   │  │ #  Nombre     Documento    Acciones  ││
   │  ├──────────────────────────────────────┤│
   │  │ 1  Juan Pérez 1020304050  ✏️ Editar ││
   │  │ 2  María López 1030405060 ✏️ Editar ││
   │  │ 3  Carlos A.   1040506070 ✏️ Editar ││
   │  └──────────────────────────────────────┘│
   │  [➕ Registrar Nuevo Paciente]         │
   └──────────────────────────────────────────┘

6. GESTIONAR MÉDICOS
   Sidebar → "👨‍⚕️ Médicos"
   - Ver lista de médicos
   - Agregar nuevo médico
   - Eliminar médico

7. VER TODAS LAS CITAS
   Sidebar → "🗓️ Todas las Citas"
   - Ver tabla de citas agendadas
   - Actualizar estado de cita
   - Cancelar cita si necesario
```

---

## 🎯 CASOS DE USO COMUNES

### Caso 1: Nuevo Paciente quiere agendar cita
```
1. Va a http://localhost:5000/
2. Hace clic en "Registrarse"
3. Completa el formulario
4. Inicia sesión
5. Va a "Reservar Cita"
6. Elige médico y fecha
7. ¡Cita agendada!
```

### Caso 2: Admin quiere crear nuevo usuario
```
1. Inicia sesión como admin
2. Ve el Dashboard
3. Hace clic en "➕ Nuevo Usuario"
4. Completa datos
5. Selecciona rol (Paciente, Admin, Médico)
6. ¡Usuario creado!
```

### Caso 3: Admin quiere ver estadísticas
```
1. Inicia sesión como admin
2. En Dashboard ve gráficos automáticamente
3. Puede filtrar por tipo de cita
4. Puede filtrar por doctor
5. El gráfico se actualiza en tiempo real
```

### Caso 4: Paciente quiere ver su perfil
```
1. Inicia sesión como paciente
2. Hace clic en "👤 Mi Perfil"
3. Ve su información personal
4. Ve todas sus citas agendadas
5. Puede ver estado de cada cita
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### "No veo el gráfico en el Dashboard"
- Verifica que tienes conexión a internet (Chart.js viene de CDN)
- Abre la consola (F12) y verifica los errores
- Recarga la página

### "No puedo crear un usuario"
- Verifica que el username y email sean únicos
- Asegúrate de escribir todos los campos
- Verifica que la contraseña tenga al menos 6 caracteres

### "El filtro no funciona"
- Verifica que existan citas en la BD
- Asegúrate de que el médico tiene citas asignadas
- Recarga el dashboard

### "No aparece el registro en la BD"
- Verifica que MySQL esté corriendo
- Revisa que los datos sean válidos
- Mira los logs en la consola de Python

---

## 📊 ESTADÍSTICAS POR TIPO

Si tienes citas de diferentes tipos:
- **General**: Médicos de medicina general
- **Odontología**: Dentistas
- **Especialista**: Otros especialistas

El gráfico muestra automáticamente citas por estado:
- 🟠 Pendiente: Esperando atención
- 🟢 Confirmada: Listo para asistir
- 🔴 Cancelada: No se realizó

---

## ✅ VALIDACIÓN RÁPIDA

Para verificar que todo funciona:

1. **Portal accesible**
   - Abre http://localhost:5000/
   - ¿Ves el portal de MEDILOGIX? ✅

2. **Registro funciona**
   - Regístrate un nuevo paciente
   - ¿Se crea usuario y paciente? ✅

3. **Login funciona**
   - Inicia sesión con admin/Admin2025*
   - ¿Ves el dashboard? ✅

4. **Gráfico aparece**
   - ¿Ves el gráfico de barras? ✅
   - ¿Se actualiza con filtros? ✅

5. **Crear usuario funciona**
   - Crea un nuevo usuario desde dashboard
   - ¿Aparece en lista de usuarios? ✅

---

## 🎓 RESUMEN VISUAL

```
┌────────────────────────────────────────────────────────────┐
│                    MEDILOGIX 2026                          │
│            Sistema de Gestión de Citas Médicas             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  USUARIO NUEVO          PACIENTE              ADMINISTRADOR│
│      ↓                      ↓                      ↓       │
│   Portal              Perfil + Citas       Dashboard       │
│   ↓                      ↓                      ↓        │
│ Registro           Ver Historial          Gráficos        │
│   ↓                      ↓                      ↓        │
│ Usuario               Agendar               Filtros        │
│   ↓                      ↓                      ↓        │
│ Perfil               Confirmar             Usuarios        │
│                                                            │
│  📊 BASE DE DATOS COMPARTIDA                             │
│  ├─ Usuarios (admin, paciente, médico)                   │
│  ├─ Pacientes (con documento, EPS)                       │
│  ├─ Médicos (con especialidad)                           │
│  ├─ Citas (con estado y fechas 2026)                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🚀 ¡LISTO PARA USAR!

Tu sistema MEDILOGIX está completamente funcional.

**Características principales:**
- ✅ Portal profesional
- ✅ Registro público
- ✅ Dashboard con gráficos
- ✅ Gestión de usuarios
- ✅ Filtros interactivos
- ✅ Branding MEDILOGIX
- ✅ Año 2026 actualizado

**¡Disfruta tu plataforma de citas médicas! 🏥**
