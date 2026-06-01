# Plataforma Estudiantes Marroquíes en España

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-WebSocket-red?logo=redis)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet?logo=railway)
![License](https://img.shields.io/badge/Licencia-MIT-yellow)

---

## Descripción del Proyecto

**Plataforma Estudiantes Marroquíes en España** es una aplicación web desarrollada como Proyecto de Fin de Estudios (DAM — DIGITECH 2026). Su objetivo es centralizar los recursos y servicios que necesita un estudiante marroquí al llegar a España: encontrar alojamiento, contactar con profesionales (abogados, orientadores), comunicarse en tiempo real con otros estudiantes y reportar situaciones irregulares.

### Problema que resuelve

Los estudiantes marroquíes en España se enfrentan a múltiples obstáculos al inicio de su estancia:
- Dificultad para encontrar alojamiento fiable y asequible.
- Falta de acceso a asesoramiento jurídico y académico en su idioma.
- Ausencia de una comunidad digital de apoyo entre compatriotas.
- Exposición a anuncios fraudulentos o perfiles falsos.

Esta plataforma ofrece un entorno seguro, validado por administradores, donde todos estos servicios convergen en un único lugar.

---

## Funcionalidades

- 🏠 **Módulo de Alojamiento** — publicación, búsqueda y filtrado de anuncios de pisos y habitaciones; validación por parte del administrador antes de publicar.
- 👩‍⚖️ **Directorio Profesional** — fichas de abogados y orientadores académicos validados, con especialidades, idiomas y datos de contacto.
- 💬 **Chat en Tiempo Real** — mensajería privada entre usuarios y grupos de chat por ciudad, implementado con WebSocket (Django Channels + Redis).
- 🚨 **Sistema de Denuncias** — flujo completo para reportar anuncios fraudulentos o perfiles sospechosos, con seguimiento de estado (pendiente / en revisión / resuelto).
- 🛡️ **Panel de Administración** — moderación de contenidos, validación de usuarios y anuncios, registro de actividad (audit log).
- 🔐 **Autenticación por Roles** — 5 tipos de usuario con permisos diferenciados: estudiante, abogado, orientador, propietario/agencia y administrador.

---

## Stack Tecnológico

| Capa | Tecnología | Versión |
|---|---|---|
| Lenguaje | Python | 3.11 |
| Framework web | Django | 4.x |
| ASGI Server | Daphne | 4.x |
| WebSocket | Django Channels | 4.x |
| Base de datos | PostgreSQL (Supabase) | 15 |
| Cache / Canal WebSocket | Redis | 7.x |
| Frontend | Bootstrap | 5.3 |
| Almacenamiento de archivos | Supabase Storage (S3) | — |
| Despliegue | Railway | — |
| Servidor estático | WhiteNoise | 6.x |

---

## Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener:

- Python 3.11 o superior
- `pip` y `virtualenv`
- PostgreSQL (local o cuenta en [Supabase](https://supabase.com))
- Redis (local o servicio en la nube)
- Git

---

## Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/student-platform.git
cd student-platform/plateforme_etudiants
```

### 2. Crear y activar el entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

```bash
cp .env.example .env
# Edita .env con tus valores reales
```

### 5. Aplicar las migraciones

```bash
python manage.py migrate --run-syncdb
```

### 6. Crear un superusuario administrador

```bash
python manage.py createsuperuser
```

### 7. Recopilar los archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 8. Iniciar el servidor de desarrollo

```bash
# Con soporte WebSocket (recomendado)
daphne config.asgi:application --port 8000 --bind 0.0.0.0

# O con el servidor estándar de Django (sin WebSocket)
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`.

---

## Variables de Entorno (.env)

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-...` |
| `DEBUG` | Modo depuración (`True` solo en desarrollo) | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma | `localhost,mi-app.railway.app` |
| `DATABASE_URL` | URL de conexión PostgreSQL | `postgresql://user:pass@host/db` |
| `REDIS_URL` | URL de conexión Redis | `redis://localhost:6379` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes de confianza para CSRF | `https://mi-app.railway.app` |
| `USE_SUPABASE_STORAGE` | Activar almacenamiento S3 en Supabase | `True` |
| `AWS_ACCESS_KEY_ID` | Clave de acceso Supabase Storage | `tu-access-key` |
| `AWS_SECRET_ACCESS_KEY` | Clave secreta Supabase Storage | `tu-secret-key` |
| `AWS_STORAGE_BUCKET_NAME` | Nombre del bucket S3 | `student-platform` |
| `AWS_S3_ENDPOINT_URL` | Endpoint S3 de Supabase | `https://xxx.supabase.co/storage/v1/s3` |

---

## Estructura de Carpetas

```
plateforme_etudiants/
├── config/                  # Configuración principal del proyecto
│   ├── settings.py          # Ajustes globales (BD, correo, channels…)
│   ├── urls.py              # Enrutamiento raíz
│   ├── asgi.py              # Punto de entrada ASGI (WebSocket)
│   └── wsgi.py              # Punto de entrada WSGI
│
├── core/                    # Autenticación y gestión de usuarios
│   ├── models.py            # Modelo User personalizado + ProfessionalProfile
│   ├── views.py             # Login, registro, perfil
│   ├── forms.py             # Formularios de autenticación
│   └── backends.py          # Backend de autenticación por email
│
├── housing/                 # Módulo de alojamiento
│   ├── models.py            # HousingListing + ListingPhoto
│   ├── views.py             # CRUD de anuncios, búsqueda, filtros
│   └── forms.py             # Formulario de creación de anuncios
│
├── professionals/           # Directorio de profesionales
│   ├── views.py             # Listado y detalle de abogados/orientadores
│   └── forms.py             # Formulario de perfil profesional
│
├── chat/                    # Chat en tiempo real
│   ├── consumers.py         # Consumidores WebSocket
│   ├── routing.py           # Rutas WebSocket
│   ├── models.py            # ChatGroup + Message
│   └── views.py             # Vistas de chat
│
├── reports/                 # Sistema de denuncias
│   ├── models.py            # Report (denuncias)
│   └── views.py             # Creación y gestión de denuncias
│
├── dashboard/               # Panel de administración
│   ├── models.py            # ActivityLog (registro de actividad)
│   ├── views.py             # Moderación y estadísticas
│   └── decorators.py        # Control de acceso por rol
│
├── templates/               # Plantillas HTML organizadas por módulo
├── static/                  # CSS, JS, imágenes del proyecto
├── media/                   # Archivos subidos por los usuarios
├── requirements.txt         # Dependencias Python
├── Procfile                 # Comando de inicio para Railway
└── manage.py                # CLI de Django
```

---

## Despliegue en Railway

### 1. Crear un proyecto en Railway

1. Accede a [railway.app](https://railway.app) y crea un nuevo proyecto.
2. Conecta tu repositorio de GitHub.

### 2. Añadir los servicios

En el dashboard de Railway, añade:
- **PostgreSQL** → Railway lo provisiona automáticamente (o usa Supabase).
- **Redis** → Añade el plugin Redis desde Railway.

### 3. Configurar las variables de entorno

En la sección *Variables* de tu servicio web, añade todas las variables del `.env` de producción (ver tabla anterior).

### 4. Verificar el Procfile

El archivo `Procfile` ya está configurado en la raíz del proyecto:

```
web: python manage.py collectstatic --noinput && python manage.py migrate --run-syncdb && daphne config.asgi:application --port $PORT --bind 0.0.0.0
```

Railway detecta este archivo automáticamente y ejecuta el comando al desplegar.

### 5. Desplegar

Haz push a la rama principal. Railway desplegará automáticamente la aplicación.

---

## Autores

| Nombre | Rol |
|---|---|
| Salma Moussaoui | Estudiante —  Desarrollo de Backend |
| DIGITECH | Centro de Formación — DAM 2026 |

---

## Licencia

Este proyecto está bajo la licencia **MIT**.

```
MIT License

Copyright (c) 2026 Salma Moussaoui — DIGITECH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
