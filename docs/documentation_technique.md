# Documentación Técnica — Plataforma Estudiantes Marroquíes en España

**Proyecto de Fin de Estudios — DAM — DIGITECH 2026**
Autora: Salma Moussaoui

---

## Índice

1. [Arquitectura MVT](#1-arquitectura-mvt)
2. [Stack Técnico Detallado](#2-stack-técnico-detallado)
3. [Estructura de Carpetas Django](#3-estructura-de-carpetas-django)
4. [Modelos de Datos](#4-modelos-de-datos)
5. [Sistema de Roles y Autenticación](#5-sistema-de-roles-y-autenticación)
6. [Implementación del Chat WebSocket](#6-implementación-del-chat-websocket)
7. [Vistas y URLs Principales](#7-vistas-y-urls-principales)
8. [Configuración de Variables de Entorno](#8-configuración-de-variables-de-entorno)
9. [Pipeline de Despliegue Railway + Supabase](#9-pipeline-de-despliegue-railway--supabase)
10. [Seguridad](#10-seguridad)

---

## 1. Arquitectura MVT

Django implementa el patrón **MVT (Model – View – Template)**, una variante del clásico MVC donde el "Controller" es gestionado por el propio framework.

```
Solicitud HTTP / WebSocket
         │
         ▼
┌─────────────────────────────┐
│         ASGI / Daphne       │  ← Servidor de entrada (HTTP + WS)
└─────────────┬───────────────┘
              │
     ┌────────┴────────┐
     │    URL Router   │  ← config/urls.py + chat/routing.py
     └────────┬────────┘
              │
  ┌───────────┴────────────┐
  │   View / Consumer      │  ← Lógica de negocio
  │  (views.py / consumers)│
  └───────────┬────────────┘
              │
    ┌─────────┴──────────┐
    │       Model        │  ← ORM Django → PostgreSQL (Supabase)
    └─────────┬──────────┘
              │
    ┌─────────┴──────────┐
    │      Template      │  ← HTML + Bootstrap 5
    └────────────────────┘
```

### Capas del proyecto

| Capa | Responsabilidad | Ubicación |
|---|---|---|
| **Routing** | Despacho de peticiones HTTP y WebSocket | `config/urls.py`, `chat/routing.py` |
| **View / Consumer** | Lógica de negocio, validaciones, respuestas | `*/views.py`, `chat/consumers.py` |
| **Model** | Definición de datos y queries ORM | `*/models.py` |
| **Template** | Renderizado HTML | `templates/` |
| **Form** | Validación de entrada de usuario | `*/forms.py` |
| **Admin** | Panel de gestión integrado de Django | `*/admin.py` |
| **Middleware** | Seguridad, sesiones, CSRF, WhiteNoise | `config/settings.py` |

---

## 2. Stack Técnico Detallado

### Backend

| Componente | Tecnología | Versión | Rol |
|---|---|---|---|
| Lenguaje | Python | 3.11 | Base de la aplicación |
| Framework | Django | 4.x | MVT, ORM, Admin |
| ASGI Server | Daphne | 4.x | HTTP + WebSocket en producción |
| WebSocket | Django Channels | 4.x | Mensajería en tiempo real |
| Canal de mensajes | channels-redis | 4.x | Backend Redis para Channels |
| ORM / BD | psycopg2-binary | 2.9 | Adaptador PostgreSQL |
| Variables de entorno | python-decouple | 3.8 | Gestión segura de `.env` |
| URLs de BD | dj-database-url | 2.x | Parseo de `DATABASE_URL` |
| Imágenes | Pillow | 10.x | Procesamiento de fotos |
| Archivos estáticos | WhiteNoise | 6.x | Servir estáticos en producción |
| Almacenamiento S3 | django-storages + boto3 | — | Supabase Storage |

### Frontend

| Componente | Tecnología | Versión |
|---|---|---|
| Framework CSS | Bootstrap | 5.3 |
| Iconos | Bootstrap Icons | 1.11 |
| JavaScript | Vanilla JS | ES6+ |
| WebSocket cliente | Web API nativa | — |

### Infraestructura

| Servicio | Proveedor | Uso |
|---|---|---|
| Base de datos | Supabase (PostgreSQL 15) | Datos persistentes |
| Almacenamiento | Supabase Storage (S3) | Fotos de anuncios y perfiles |
| Cache / Channels | Redis 7.x | Canal WebSocket y sesiones |
| Despliegue | Railway | Hosting del backend |

---

## 3. Estructura de Carpetas Django

```
plateforme_etudiants/
│
├── config/                       # Paquete de configuración del proyecto
│   ├── __init__.py
│   ├── settings.py               # Configuración global (BD, apps, seguridad…)
│   ├── urls.py                   # Enrutamiento raíz
│   ├── asgi.py                   # Punto de entrada ASGI (HTTP + WebSocket)
│   └── wsgi.py                   # Punto de entrada WSGI (fallback)
│
├── core/                         # App: autenticación y gestión de usuarios
│   ├── models.py                 # User personalizado, ProfessionalProfile
│   ├── views.py                  # Login, registro, perfil, edición
│   ├── forms.py                  # Formularios de auth y perfil
│   ├── backends.py               # Backend auth por email
│   ├── context_processors.py     # Variables globales de contexto
│   ├── templatetags/
│   │   └── photo_tags.py         # Filtros de plantilla para fotos
│   ├── admin.py                  # Registro de modelos en el admin
│   ├── urls.py                   # Rutas de autenticación y perfiles
│   └── migrations/               # Historial de migraciones
│
├── housing/                      # App: anuncios de alojamiento
│   ├── models.py                 # HousingListing, ListingPhoto
│   ├── views.py                  # CRUD anuncios, búsqueda, moderación
│   ├── forms.py                  # Formulario de anuncio
│   ├── admin.py                  # Admin de listings
│   └── urls.py                   # Rutas del módulo housing
│
├── professionals/                # App: directorio de profesionales
│   ├── models.py                 # (vacío — usa core.ProfessionalProfile)
│   ├── views.py                  # Listado abogados, orientadores, detalle
│   ├── forms.py                  # Formulario de perfil profesional
│   └── urls.py                   # Rutas del directorio
│
├── chat/                         # App: mensajería en tiempo real
│   ├── models.py                 # ChatGroup, Message
│   ├── consumers.py              # Consumidores WebSocket (privado + grupo)
│   ├── routing.py                # Rutas WebSocket (ASGI)
│   ├── views.py                  # Vistas HTTP del chat
│   ├── forms.py                  # Formulario de mensaje
│   └── urls.py                   # Rutas HTTP del chat
│
├── reports/                      # App: sistema de denuncias
│   ├── models.py                 # Report
│   ├── views.py                  # Crear denuncia, listado admin
│   ├── forms.py                  # Formulario de denuncia
│   └── urls.py                   # Rutas del módulo
│
├── dashboard/                    # App: panel de administración
│   ├── models.py                 # ActivityLog
│   ├── views.py                  # Dashboard, moderación, estadísticas
│   ├── decorators.py             # Control de acceso por rol
│   ├── forms.py                  # Formularios de moderación
│   └── urls.py                   # Rutas del dashboard
│
├── templates/                    # Plantillas HTML
│   ├── base.html                 # Base genérica
│   ├── base_app.html             # Base con navbar autenticado
│   ├── base_landing.html         # Base para la landing pública
│   ├── index.html / landing.html # Página de inicio
│   ├── 403.html / 404.html       # Páginas de error
│   ├── core/                     # Login, registro, perfiles
│   ├── housing/                  # Listado, detalle, formularios
│   ├── professionals/            # Directorio, fichas
│   ├── chat/                     # Chat privado, grupos
│   ├── reports/                  # Formulario de denuncia
│   ├── dashboard/                # Panel admin, tablas de moderación
│   └── partials/                 # Fragmentos reutilizables (navbar, footer…)
│
├── static/                       # Archivos estáticos fuente
│   ├── css/                      # Hojas de estilo personalizadas
│   ├── js/                       # Scripts JavaScript
│   └── img/                      # Imágenes del proyecto
│
├── staticfiles/                  # Salida de collectstatic (producción)
├── media/                        # Archivos subidos por los usuarios
│   ├── listings/                 # Fotos de anuncios
│   └── profiles/                 # Fotos de perfil
│
├── manage.py                     # CLI de Django
├── requirements.txt              # Dependencias Python
├── Procfile                      # Comando de inicio Railway
└── .env / .env.example           # Variables de entorno
```

---

## 4. Modelos de Datos

### Diagrama de relaciones

```
User (core)
 ├── HousingListing (housing)     [FK: owner → User]
 │    └── ListingPhoto             [FK: listing → HousingListing]
 ├── ProfessionalProfile (core)   [OneToOne: user → User]
 ├── Message (chat)               [FK: sender, receiver → User]
 │                                [FK: group → ChatGroup]
 ├── ChatGroup (chat)             [M2M: members → User]
 ├── Report (reports)             [FK: reporter, reported_user → User]
 │                                [FK: listing → HousingListing]
 └── ActivityLog (dashboard)      [FK: user → User]
```

---

### 4.1 Modelo `User` (app: `core`)

Extiende `AbstractUser`. La autenticación se realiza por **email** en lugar de nombre de usuario.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `email` | EmailField (unique) | Usado como USERNAME_FIELD |
| `username` | CharField | Nombre de usuario (opcional) |
| `first_name` | CharField | Nombre |
| `last_name` | CharField | Apellido |
| `role` | CharField (choices) | `student`, `lawyer`, `orientation`, `housing`, `admin` |
| `city` | CharField | Ciudad de residencia |
| `phone` | CharField (nullable) | Teléfono de contacto |
| `photo` | ImageField (nullable) | Foto de perfil |
| `is_validated` | BooleanField | Usuario validado por el admin |
| `date_joined` | DateTimeField | Fecha de registro (auto) |

**Métodos relevantes:**
- `is_pro()` → `True` si el rol es `lawyer` o `orientation`
- `get_initials()` → iniciales del nombre completo
- `get_photo_url()` → URL de la foto o avatar por defecto

---

### 4.2 Modelo `ProfessionalProfile` (app: `core`)

Perfil extendido para profesionales, creado automáticamente vía señal Django.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `user` | OneToOneField → `User` | Profesional asociado |
| `bio` | TextField | Descripción profesional |
| `speciality` | CharField | Especialidad (derecho, orientación…) |
| `languages` | CharField | Idiomas (es, fr, ar…) |
| `website` | URLField (nullable) | Sitio web personal |
| `linkedin` | URLField (nullable) | Perfil LinkedIn |

---

### 4.3 Modelo `HousingListing` (app: `housing`)

Anuncios de alojamiento publicados por propietarios o agencias.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `owner` | ForeignKey → `User` | Propietario del anuncio |
| `title` | CharField | Título del anuncio |
| `description` | TextField | Descripción detallada |
| `type` | CharField (choices) | `room`, `apartment`, `shared` |
| `price` | DecimalField | Precio mensual en euros |
| `city` | CharField | Ciudad donde se ubica |
| `photo` | ImageField (nullable) | Foto principal |
| `is_approved` | BooleanField | Aprobado por el admin (default: False) |
| `is_active` | BooleanField | Visible en el listado (default: True) |
| `created_at` | DateTimeField (auto) | Fecha de creación |

---

### 4.4 Modelo `ListingPhoto` (app: `housing`)

Galería de imágenes adicionales por anuncio.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `listing` | ForeignKey → `HousingListing` | Anuncio al que pertenece |
| `image` | ImageField | Imagen de la galería |
| `ordre` | IntegerField | Orden de visualización |

---

### 4.5 Modelo `ChatGroup` (app: `chat`)

Grupos de chat por ciudad o temática.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `name` | CharField | Nombre del grupo |
| `city` | CharField | Ciudad asociada |
| `members` | ManyToManyField → `User` | Miembros del grupo |
| `created_at` | DateTimeField (auto) | Fecha de creación |

---

### 4.6 Modelo `Message` (app: `chat`)

Mensajes privados (1 a 1) y mensajes de grupo.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `sender` | ForeignKey → `User` | Remitente |
| `receiver` | ForeignKey → `User` (nullable) | Destinatario (chat privado) |
| `group` | ForeignKey → `ChatGroup` (nullable) | Grupo destino (chat grupal) |
| `content` | TextField | Contenido del mensaje |
| `attachment` | FileField (nullable) | Archivo adjunto |
| `is_read` | BooleanField | Leído por el destinatario |
| `sent_at` | DateTimeField (auto) | Fecha y hora de envío |

> Un mensaje pertenece **exclusivamente** a un chat privado (`receiver != null`) o a un grupo (`group != null`), nunca a ambos.

---

### 4.7 Modelo `Report` (app: `reports`)

Denuncias de usuarios o anuncios.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `reporter` | ForeignKey → `User` | Usuario que denuncia |
| `reported_user` | ForeignKey → `User` (nullable) | Usuario denunciado |
| `listing` | ForeignKey → `HousingListing` (nullable) | Anuncio denunciado |
| `reason` | CharField (choices) | `scam`, `inappropriate_behavior`, `fake_profile`, `other` |
| `description` | TextField | Descripción detallada |
| `status` | CharField (choices) | `pending`, `reviewing`, `resolved` |
| `created_at` | DateTimeField (auto) | Fecha de la denuncia |

---

### 4.8 Modelo `ActivityLog` (app: `dashboard`)

Registro de auditoría de acciones administrativas.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (PK) | Identificador único |
| `user` | ForeignKey → `User` | Admin que ejecutó la acción |
| `action` | CharField | Descripción de la acción |
| `target_type` | CharField (choices) | `user`, `listing`, `report`, `group` |
| `target_id` | IntegerField | ID del objeto afectado |
| `ip_address` | GenericIPAddressField | IP del administrador |
| `created_at` | DateTimeField (auto) | Fecha de la acción |

---

## 5. Sistema de Roles y Autenticación

### 5.1 Modelo de autenticación

La autenticación se basa en **email + contraseña** gracias a un backend personalizado:

```python
# core/backends.py
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
```

En `settings.py`:
```python
AUTH_USER_MODEL = 'core.User'
AUTHENTICATION_BACKENDS = ['core.backends.EmailBackend']
```

### 5.2 Roles y permisos

| Rol (`role`) | Descripción | Permisos clave |
|---|---|---|
| `student` | Estudiante registrado | Buscar alojamiento, chatear, denunciar |
| `lawyer` | Abogado validado | Perfil profesional, chat, denunciar |
| `orientation` | Orientador académico | Perfil profesional, chat, denunciar |
| `housing` | Propietario o agencia | Publicar y gestionar anuncios |
| `admin` | Administrador de la plataforma | Acceso total al dashboard |

### 5.3 Control de acceso

El control de acceso se implementa mediante:

1. **Decoradores de Django** — `@login_required` para vistas que requieren autenticación.
2. **Decoradores personalizados** (`dashboard/decorators.py`) — comprueban el rol del usuario.
3. **Verificación en vistas** — comprobaciones explícitas de `user.role` y `user.is_validated`.

```python
# Ejemplo de decorador de rol (dashboard/decorators.py)
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
```

---

## 6. Implementación del Chat WebSocket

### 6.1 Arquitectura del chat

```
Cliente (navegador)
      │  WebSocket ws://…/ws/chat/privado/<user_id>/
      │  WebSocket ws://…/ws/chat/grupo/<group_id>/
      ▼
  Daphne (ASGI)
      │
      ▼
  Django Channels
      │  ChannelLayer (Redis)
      ▼
  Consumer (chat/consumers.py)
      │
      ▼
  Base de datos (Message guardado)
```

### 6.2 Configuración del Channel Layer (settings.py)

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL", default="redis://localhost:6379")],
        },
    },
}
```

### 6.3 Enrutamiento WebSocket (chat/routing.py)

```python
websocket_urlpatterns = [
    re_path(r"ws/chat/privado/(?P<user_id>\d+)/$", PrivateChatConsumer.as_asgi()),
    re_path(r"ws/chat/grupo/(?P<group_id>\d+)/$",  GroupChatConsumer.as_asgi()),
]
```

### 6.4 Configuración ASGI (config/asgi.py)

```python
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})
```

### 6.5 Ciclo de vida de un mensaje WebSocket

1. El cliente abre una conexión WebSocket.
2. `connect()` — el consumidor verifica la autenticación y une el canal al grupo Redis.
3. `receive()` — recibe el JSON del mensaje, lo persiste en BD y lo distribuye al grupo.
4. `chat_message()` — emite el mensaje a todos los sockets del grupo.
5. `disconnect()` — elimina el canal del grupo Redis.

```python
# Fragmento simplificado del consumer privado
class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"chat_{min(self.scope['user'].id, self.user_id)}_{max(...)}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Guardar mensaje en BD (sync_to_async)
        await self.save_message(data['message'])
        # Emitir al grupo
        await self.channel_layer.group_send(self.room_name, {
            "type": "chat_message",
            "message": data['message'],
            "sender": self.scope['user'].username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
```

---

## 7. Vistas y URLs Principales

### App `core`

| URL | Vista | Descripción |
|---|---|---|
| `/` | `landing_view` | Página de inicio pública |
| `/login/` | `login_view` | Inicio de sesión |
| `/register/` | `register_view` | Registro de usuario |
| `/logout/` | `logout_view` | Cierre de sesión |
| `/perfil/` | `profile_view` | Ver perfil propio |
| `/perfil/editar/` | `edit_profile_view` | Editar perfil |

### App `housing`

| URL | Vista | Descripción |
|---|---|---|
| `/alojamiento/` | `listing_list_view` | Listado de anuncios aprobados |
| `/alojamiento/<id>/` | `listing_detail_view` | Detalle de un anuncio |
| `/alojamiento/crear/` | `listing_create_view` | Crear anuncio (rol housing) |
| `/alojamiento/<id>/editar/` | `listing_edit_view` | Editar anuncio propio |
| `/alojamiento/<id>/eliminar/` | `listing_delete_view` | Eliminar anuncio propio |
| `/mis-anuncios/` | `my_listings_view` | Anuncios del propietario |

### App `professionals`

| URL | Vista | Descripción |
|---|---|---|
| `/abogados/` | `lawyer_list_view` | Directorio de abogados |
| `/orientadores/` | `advisor_list_view` | Directorio de orientadores |
| `/profesional/<id>/` | `professional_detail_view` | Ficha de profesional |

### App `chat`

| URL | Vista | Descripción |
|---|---|---|
| `/chat/` | `chat_list_view` | Lista de conversaciones |
| `/chat/privado/<user_id>/` | `private_chat_view` | Chat privado con un usuario |
| `/chat/grupos/` | `group_list_view` | Lista de grupos |
| `/chat/grupo/<id>/` | `group_chat_view` | Chat de grupo |

### App `reports`

| URL | Vista | Descripción |
|---|---|---|
| `/reports/crear/` | `create_report_view` | Crear denuncia |
| `/reports/mis-denuncias/` | `my_reports_view` | Denuncias del usuario |

### App `dashboard`

| URL | Vista | Descripción |
|---|---|---|
| `/dashboard/` | `admin_dashboard_view` | Panel principal (admin) |
| `/dashboard/usuarios/` | `user_list_view` | Gestión de usuarios |
| `/dashboard/anuncios/` | `listing_moderation_view` | Moderación de anuncios |
| `/dashboard/denuncias/` | `report_management_view` | Gestión de denuncias |

---

## 8. Configuración de Variables de Entorno

### Desarrollo (`.env`)

```env
SECRET_KEY=django-insecure-clave-solo-para-desarrollo
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/student_platform
REDIS_URL=redis://localhost:6379
USE_SUPABASE_STORAGE=False
```

### Producción (Railway)

```env
SECRET_KEY=<clave-aleatoria-segura-50-caracteres>
DEBUG=False
ALLOWED_HOSTS=mi-app.railway.app
DATABASE_URL=postgresql://postgres:<password>@db.xxx.supabase.co:5432/postgres
REDIS_URL=redis://default:<password>@xxx.railway.app:6379
CSRF_TRUSTED_ORIGINS=https://mi-app.railway.app
USE_SUPABASE_STORAGE=True
AWS_ACCESS_KEY_ID=<supabase-s3-key>
AWS_SECRET_ACCESS_KEY=<supabase-s3-secret>
AWS_STORAGE_BUCKET_NAME=student-platform
AWS_S3_ENDPOINT_URL=https://<project-id>.supabase.co/storage/v1/s3
```

### Diferencias clave dev vs prod

| Variable | Desarrollo | Producción |
|---|---|---|
| `DEBUG` | `True` | `False` |
| `DATABASE_URL` | SQLite o PostgreSQL local | Supabase PostgreSQL |
| `USE_SUPABASE_STORAGE` | `False` (local `media/`) | `True` (S3) |
| `SECURE_*` cookies | Desactivadas | Activadas |

---

## 9. Pipeline de Despliegue Railway + Supabase

```
Desarrollo local
      │  git push origin main
      ▼
   GitHub
      │  Webhook → Railway CI
      ▼
Railway Build
  ① pip install -r requirements.txt
  ② Procfile: python manage.py collectstatic --noinput
  ③ Procfile: python manage.py migrate --run-syncdb
  ④ Procfile: daphne config.asgi:application --port $PORT --bind 0.0.0.0
      │
      ├──► Supabase PostgreSQL  (DATABASE_URL)
      ├──► Redis Railway        (REDIS_URL)
      └──► Supabase Storage S3 (AWS_* variables)
```

### Ajustes necesarios en settings.py para Railway

```python
# Proxy SSL de Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookies seguras en producción
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# HSTS
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
```

---

## 10. Seguridad

### 10.1 Protección CSRF

Django activa el middleware CSRF por defecto. Todos los formularios POST incluyen `{% csrf_token %}`. Para orígenes externos (Railway), se configura:

```python
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
```

### 10.2 Validación de entrada

- **Formularios Django** — cada `Form` o `ModelForm` valida tipos, longitudes y unicidad antes de guardar.
- **ORM Django** — las consultas usan el ORM parametrizado, lo que previene inyección SQL.
- **Pillow** — las imágenes subidas se procesan con Pillow para evitar archivos maliciosos.

### 10.3 Control de acceso

- `@login_required` — impide el acceso de usuarios no autenticados.
- `@admin_required` — restringe las vistas del dashboard al rol `admin`.
- Comprobaciones explícitas `user.role` en las vistas que modifican datos sensibles.
- Los anuncios con `is_approved=False` no se muestran en el listado público.
- Los usuarios con `is_validated=False` tienen acceso limitado.

### 10.4 Seguridad de contraseñas

Django aplica validadores de contraseña configurables:

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### 10.5 Cabeceras de seguridad HTTP

| Cabecera | Activación |
|---|---|
| `SECURE_HSTS_SECONDS` | Habilitado en producción (31536000 s) |
| `SECURE_BROWSER_XSS_FILTER` | Activado por defecto en Django |
| `X_FRAME_OPTIONS` | `DENY` (previene clickjacking) |
| `SESSION_COOKIE_SECURE` | `True` en producción |
| `CSRF_COOKIE_SECURE` | `True` en producción |
