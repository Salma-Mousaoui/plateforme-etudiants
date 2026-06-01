# Documentación Funcional — Plataforma Estudiantes Marroquíes en España

**Proyecto de Fin de Estudios — DAM — DIGITECH 2026**
Autora: Salma Moussaoui

---

## Índice

1. [Presentación y Contexto del Proyecto](#1-presentación-y-contexto-del-proyecto)
2. [Actores del Sistema](#2-actores-del-sistema)
3. [Casos de Uso por Actor](#3-casos-de-uso-por-actor)
4. [Módulo de Alojamiento](#4-módulo-de-alojamiento)
5. [Módulo de Directorio Profesional](#5-módulo-de-directorio-profesional)
6. [Módulo de Chat en Tiempo Real](#6-módulo-de-chat-en-tiempo-real)
7. [Panel de Administración](#7-panel-de-administración)
8. [Sistema de Denuncias](#8-sistema-de-denuncias)
9. [Reglas de Negocio y Restricciones de Acceso](#9-reglas-de-negocio-y-restricciones-de-acceso)
10. [Descripción de las Pantallas Principales](#10-descripción-de-las-pantallas-principales)

---

## 1. Presentación y Contexto del Proyecto

### 1.1 Descripción general

La **Plataforma Estudiantes Marroquíes en España** es una aplicación web multi-rol diseñada para centralizar los recursos que necesita un estudiante marroquí al llegar o residir en España. La plataforma actúa como punto de encuentro entre estudiantes, profesionales (abogados y orientadores académicos), propietarios de alojamiento y administradores de la plataforma.

### 1.2 Problema identificado

Los estudiantes marroquíes en España se enfrentan habitualmente a:

- **Búsqueda de alojamiento difícil y arriesgada**: ausencia de una plataforma fiable adaptada a su situación.
- **Falta de asesoramiento jurídico accesible**: desconocimiento de derechos, dificultades con visados, contratos de alquiler.
- **Aislamiento social**: ausencia de una comunidad digital de apoyo entre compatriotas.
- **Exposición a fraudes**: anuncios falsos, perfiles fraudulentos en plataformas generales.

### 1.3 Solución aportada

La plataforma ofrece:

| Necesidad | Solución |
|---|---|
| Encontrar alojamiento seguro | Módulo de anuncios validados por admin |
| Asesoramiento jurídico/académico | Directorio de profesionales verificados |
| Comunidad y apoyo entre estudiantes | Chat privado y grupos por ciudad |
| Reportar situaciones irregulares | Sistema de denuncias con seguimiento |

### 1.4 Alcance del proyecto (PFE DAM 2026)

Este proyecto constituye el Proyecto de Fin de Estudios (PFE) del ciclo **Desarrollo de Aplicaciones Multiplataforma (DAM)** impartido en **DIGITECH** durante el curso 2025-2026.

---

## 2. Actores del Sistema

La plataforma define **5 tipos de usuarios** con permisos y funcionalidades diferenciadas.

### 2.1 Tabla de actores

| Actor | Código de rol | Descripción | Proceso de alta |
|---|---|---|---|
| **Estudiante** | `student` | Estudiante marroquí en España. Usuario principal de la plataforma. | Registro libre + validación opcional |
| **Abogado** | `lawyer` | Profesional jurídico que ofrece asesoramiento. | Registro + validación obligatoria por admin |
| **Orientador Académico** | `orientation` | Profesional de orientación educativa y universitaria. | Registro + validación obligatoria por admin |
| **Propietario / Agencia** | `housing` | Persona o empresa que publica anuncios de alojamiento. | Registro + cada anuncio requiere validación |
| **Administrador** | `admin` | Gestiona y modera toda la plataforma. | Creado directamente por superusuario |

### 2.2 Permisos por actor

| Funcionalidad | Estudiante | Abogado | Orientador | Propietario | Administrador |
|---|:---:|:---:|:---:|:---:|:---:|
| Ver anuncios de alojamiento | ✅ | ✅ | ✅ | ✅ | ✅ |
| Publicar anuncios | ❌ | ❌ | ❌ | ✅ | ✅ |
| Ver directorio profesional | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tener ficha profesional | ❌ | ✅ | ✅ | ❌ | ❌ |
| Chat privado | ✅ | ✅ | ✅ | ✅ | ✅ |
| Grupos de chat | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear denuncia | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gestionar denuncias | ❌ | ❌ | ❌ | ❌ | ✅ |
| Validar usuarios | ❌ | ❌ | ❌ | ❌ | ✅ |
| Validar anuncios | ❌ | ❌ | ❌ | ❌ | ✅ |
| Panel de administración | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 3. Casos de Uso por Actor

### 3.1 Estudiante

| ID | Caso de uso | Descripción |
|---|---|---|
| E-01 | Registrarse | Crear una cuenta con email, contraseña y rol `student` |
| E-02 | Iniciar sesión | Autenticarse con email y contraseña |
| E-03 | Editar perfil | Actualizar foto, ciudad, teléfono |
| E-04 | Buscar alojamiento | Filtrar anuncios por ciudad, tipo y precio |
| E-05 | Ver detalle de anuncio | Consultar fotos, descripción y datos del propietario |
| E-06 | Contactar propietario | Iniciar chat privado desde el anuncio |
| E-07 | Buscar profesional | Consultar el directorio de abogados u orientadores |
| E-08 | Contactar profesional | Iniciar chat privado con un profesional |
| E-09 | Participar en grupos | Unirse a grupos de chat de su ciudad |
| E-10 | Crear denuncia | Reportar un anuncio o usuario sospechoso |
| E-11 | Ver mis denuncias | Consultar el estado de sus denuncias enviadas |

### 3.2 Abogado / Orientador Académico

| ID | Caso de uso | Descripción |
|---|---|---|
| P-01 | Registrarse como profesional | Crear cuenta con rol `lawyer` u `orientation` |
| P-02 | Completar ficha profesional | Añadir bio, especialidad, idiomas y sitio web |
| P-03 | Aparecer en el directorio | Visible tras validación por el admin |
| P-04 | Recibir mensajes de estudiantes | Chat privado desde su ficha |
| P-05 | Participar en grupos de chat | Comunicarse con la comunidad |
| P-06 | Crear denuncia | Reportar comportamientos inapropiados |

### 3.3 Propietario / Agencia

| ID | Caso de uso | Descripción |
|---|---|---|
| H-01 | Registrarse como propietario | Crear cuenta con rol `housing` |
| H-02 | Publicar anuncio | Crear anuncio con fotos, descripción, precio y ciudad |
| H-03 | Gestionar mis anuncios | Ver, editar y eliminar anuncios propios |
| H-04 | Recibir consultas | Responder mensajes de estudiantes interesados |
| H-05 | Esperar validación | El anuncio solo es visible tras aprobación del admin |

### 3.4 Administrador

| ID | Caso de uso | Descripción |
|---|---|---|
| A-01 | Acceder al panel | Visualizar estadísticas generales de la plataforma |
| A-02 | Gestionar usuarios | Listar, validar, suspender o eliminar cuentas |
| A-03 | Validar anuncios | Aprobar o rechazar anuncios de alojamiento |
| A-04 | Gestionar denuncias | Revisar, cambiar estado y cerrar denuncias |
| A-05 | Gestionar grupos de chat | Crear o eliminar grupos por ciudad |
| A-06 | Consultar registro de actividad | Ver el log de acciones administrativas |

---

## 4. Módulo de Alojamiento

### 4.1 Descripción

El módulo de alojamiento permite a los propietarios y agencias publicar anuncios de pisos, habitaciones o pisos compartidos. Los estudiantes pueden buscar y filtrar estos anuncios y contactar directamente con el propietario mediante el chat integrado.

### 4.2 Flujo de publicación de un anuncio

```
Propietario
    │  Rellena formulario (título, descripción, tipo, precio, ciudad, fotos)
    ▼
Sistema guarda el anuncio con is_approved = False
    │
    ▼
Administrador recibe notificación en el panel
    │
    ├── Aprueba → is_approved = True → Anuncio visible en el listado
    └── Rechaza → El propietario es notificado (posible mensaje explicativo)
```

### 4.3 Tipos de alojamiento

| Código | Descripción |
|---|---|
| `room` | Habitación individual en piso compartido |
| `apartment` | Piso completo en alquiler |
| `shared` | Piso compartido (roommates) |

### 4.4 Filtros de búsqueda disponibles

| Filtro | Tipo | Descripción |
|---|---|---|
| Ciudad | Select | Filtrar por ciudad de España |
| Tipo de alojamiento | Select | Habitación, apartamento, compartido |
| Precio máximo | Número | Rango de precio mensual en euros |

### 4.5 Galería de fotos

Cada anuncio puede tener:
- Una **foto principal** (`HousingListing.photo`) mostrada en el listado.
- Una **galería adicional** de imágenes (`ListingPhoto`) mostrada en la página de detalle, con orden configurable.

### 4.6 Validación y moderación

- Un anuncio **no aprobado** (`is_approved=False`) **no aparece** en ningún listado público.
- El propietario puede ver sus anuncios pendientes en "Mis anuncios".
- El administrador puede aprobar o rechazar desde el panel de moderación.
- Un anuncio puede ser desactivado (`is_active=False`) sin eliminarlo, manteniendo el historial.

---

## 5. Módulo de Directorio Profesional

### 5.1 Descripción

El directorio profesional agrupa a abogados y orientadores académicos que han sido validados por el administrador de la plataforma. Los estudiantes pueden consultar sus fichas y contactarlos directamente.

### 5.2 Tipos de profesionales

| Tipo | Rol | Especialidades típicas |
|---|---|---|
| Abogado | `lawyer` | Derecho de extranjería, visados, contratos de alquiler |
| Orientador Académico | `orientation` | Convalidación de títulos, acceso a universidades, becas |

### 5.3 Contenido de una ficha profesional

| Campo | Descripción |
|---|---|
| Nombre y apellidos | Del modelo `User` |
| Foto de perfil | Imagen del usuario |
| Especialidad | Área de experiencia |
| Idiomas | Idiomas en los que atiende (español, francés, árabe…) |
| Ciudad | Ubicación del profesional |
| Bio | Descripción de su trayectoria y servicios |
| Teléfono | Dato de contacto (opcional) |
| Sitio web / LinkedIn | Enlace externo (opcional) |

### 5.4 Proceso de validación de un profesional

1. El profesional se registra seleccionando rol `lawyer` u `orientation`.
2. Completa su ficha profesional (especialidad, bio, idiomas).
3. El administrador revisa el perfil en el panel.
4. Tras la validación (`is_validated=True`), el profesional aparece en el directorio.
5. Antes de la validación, el perfil no es visible públicamente.

### 5.5 Contacto con un profesional

Desde la ficha del profesional, el estudiante puede iniciar un **chat privado** directamente, sin necesidad de copiar ningún dato de contacto.

---

## 6. Módulo de Chat en Tiempo Real

### 6.1 Descripción

El módulo de chat permite la comunicación instantánea entre todos los usuarios de la plataforma. Implementa dos modalidades: chat privado (1 a 1) y grupos de chat por ciudad.

### 6.2 Chat Privado

| Característica | Detalle |
|---|---|
| Acceso | Desde el perfil de un usuario, desde un anuncio o desde la lista de chats |
| Participantes | Exactamente 2 usuarios |
| Historial | Los mensajes se persisten en la base de datos |
| Indicador de leído | Campo `is_read` en el modelo `Message` |
| Archivos adjuntos | El modelo soporta adjuntos (`attachment`) |

**Flujo de un mensaje privado:**
1. El remitente escribe el mensaje en el formulario de chat.
2. El mensaje se envía vía WebSocket al servidor.
3. El consumidor lo guarda en la base de datos.
4. El mensaje se entrega instantáneamente al destinatario si está conectado.
5. Si el destinatario no está conectado, verá el mensaje al abrir la conversación.

### 6.3 Grupos de Chat por Ciudad

| Característica | Detalle |
|---|---|
| Creación | Solo el administrador puede crear grupos |
| Organización | Cada grupo está asociado a una ciudad española |
| Adhesión | Cualquier usuario puede unirse a los grupos de su ciudad |
| Mensajes | Visibles para todos los miembros del grupo |

**Ejemplo de grupos típicos:**
- "Estudiantes en Madrid"
- "Estudiantes en Barcelona"
- "Noticias y Convocatorias"
- "Alojamiento Urgente"

### 6.4 Lista de conversaciones

La pantalla de inicio del chat muestra:
- Lista de conversaciones privadas recientes, con nombre del interlocutor y último mensaje.
- Lista de grupos a los que pertenece el usuario.
- Indicador de mensajes no leídos.

---

## 7. Panel de Administración

### 7.1 Descripción

El panel de administración es accesible exclusivamente a los usuarios con rol `admin`. Centraliza todas las herramientas de moderación y supervisión de la plataforma.

### 7.2 Secciones del panel

#### Dashboard principal

| Elemento | Descripción |
|---|---|
| Contador de usuarios | Total de usuarios registrados y validados |
| Contador de anuncios | Total publicados / pendientes de validación |
| Contador de denuncias | Total pendientes / en revisión / resueltas |
| Actividad reciente | Últimas acciones registradas en el `ActivityLog` |

#### Gestión de usuarios

| Acción | Descripción |
|---|---|
| Listar usuarios | Tabla con todos los usuarios, rol y estado |
| Validar usuario | Cambiar `is_validated` a `True` para profesionales |
| Suspender usuario | Desactivar la cuenta sin eliminarla |
| Eliminar usuario | Eliminar la cuenta del sistema |
| Filtrar por rol | Ver solo estudiantes, profesionales, propietarios |

#### Moderación de anuncios

| Acción | Descripción |
|---|---|
| Listar anuncios pendientes | Anuncios con `is_approved=False` |
| Aprobar anuncio | `is_approved = True` → anuncio visible |
| Rechazar anuncio | Notificar al propietario con motivo |
| Desactivar anuncio | `is_active = False` → se oculta sin borrar |
| Eliminar anuncio | Borrado definitivo |

#### Gestión de denuncias

| Acción | Descripción |
|---|---|
| Listar denuncias | Tabla con todas las denuncias y su estado |
| Ver detalle | Descripción completa y contexto de la denuncia |
| Cambiar estado | `pending` → `reviewing` → `resolved` |
| Tomar medidas | Desde la denuncia, ir directamente al usuario o anuncio afectado |

#### Registro de actividad (Audit Log)

El `ActivityLog` registra automáticamente cada acción administrativa:
- Quién la realizó (admin)
- Qué acción se ejecutó
- Sobre qué objeto (usuario, anuncio, denuncia, grupo)
- Cuándo y desde qué IP

---

## 8. Sistema de Denuncias

### 8.1 Descripción

El sistema de denuncias permite a cualquier usuario autenticado reportar comportamientos irregulares: anuncios fraudulentos, perfiles falsos o comportamientos inapropiados.

### 8.2 Tipos de denuncia

| Motivo (`reason`) | Descripción |
|---|---|
| `scam` | Estafa o fraude (anuncio o usuario) |
| `inappropriate_behavior` | Comportamiento inapropiado en el chat |
| `fake_profile` | Perfil falso o suplantación de identidad |
| `other` | Otro motivo (con descripción libre) |

### 8.3 Flujo completo de una denuncia

```
Usuario autenticado
    │  Hace clic en "Denunciar" en un anuncio o perfil
    ▼
Formulario de denuncia
    │  Selecciona motivo + escribe descripción
    ▼
Denuncia guardada con status = "pending"
    │
    ▼
Administrador ve la denuncia en el panel
    │  Cambia estado a "reviewing"
    ▼
Administrador investiga (accede al perfil/anuncio denunciado)
    │
    ├── Denuncia fundada → Toma medidas (suspensión, eliminación)
    │                    → Estado: "resolved"
    └── Denuncia infundada → Archiva la denuncia
                           → Estado: "resolved"
    ▼
El usuario denunciante puede ver el estado actualizado
en su sección "Mis denuncias"
```

### 8.4 Estados de una denuncia

| Estado | Código | Significado |
|---|---|---|
| Pendiente | `pending` | Recibida, aún no revisada |
| En revisión | `reviewing` | El administrador está investigando |
| Resuelta | `resolved` | Proceso completado (con o sin sanción) |

### 8.5 Objeto de la denuncia

Una denuncia puede referirse a:
- Un **anuncio de alojamiento** (`listing != null`)
- Un **usuario** (`reported_user != null`)

Nunca a ambos simultáneamente.

---

## 9. Reglas de Negocio y Restricciones de Acceso

### 9.1 Reglas de autenticación

| Regla | Descripción |
|---|---|
| RN-01 | El email debe ser único en el sistema. |
| RN-02 | La autenticación se realiza con email, no con nombre de usuario. |
| RN-03 | Los usuarios no autenticados solo pueden ver la landing page. |
| RN-04 | Los profesionales deben ser validados para aparecer en el directorio. |

### 9.2 Reglas del módulo de alojamiento

| Regla | Descripción |
|---|---|
| RN-05 | Solo los usuarios con rol `housing` o `admin` pueden crear anuncios. |
| RN-06 | Un anuncio solo es visible si `is_approved=True` y `is_active=True`. |
| RN-07 | Solo el propietario del anuncio o un admin puede editarlo o eliminarlo. |
| RN-08 | Un propietario solo puede ver sus propios anuncios en "Mis anuncios". |

### 9.3 Reglas del directorio profesional

| Regla | Descripción |
|---|---|
| RN-09 | Solo los usuarios con rol `lawyer` u `orientation` tienen ficha profesional. |
| RN-10 | Un profesional aparece en el directorio solo si `is_validated=True`. |
| RN-11 | La ficha profesional se crea automáticamente al registrarse como profesional. |

### 9.4 Reglas del chat

| Regla | Descripción |
|---|---|
| RN-12 | Solo los usuarios autenticados pueden acceder al chat. |
| RN-13 | Un usuario no puede enviarse mensajes a sí mismo. |
| RN-14 | Solo el administrador puede crear o eliminar grupos de chat. |
| RN-15 | Los mensajes de grupo son visibles para todos los miembros. |

### 9.5 Reglas del sistema de denuncias

| Regla | Descripción |
|---|---|
| RN-16 | Solo los usuarios autenticados pueden crear denuncias. |
| RN-17 | Un usuario no puede denunciarse a sí mismo. |
| RN-18 | Solo el administrador puede ver y gestionar todas las denuncias. |
| RN-19 | Un usuario solo puede ver sus propias denuncias. |

### 9.6 Reglas del panel de administración

| Regla | Descripción |
|---|---|
| RN-20 | Solo los usuarios con rol `admin` pueden acceder al dashboard. |
| RN-21 | Toda acción administrativa queda registrada en el `ActivityLog`. |
| RN-22 | El administrador no puede eliminarse a sí mismo. |

---

## 10. Descripción de las Pantallas Principales

### 10.1 Landing Page (`/`)

Página pública de presentación de la plataforma. Contiene:
- Cabecera con nombre y eslogan de la plataforma.
- Sección de características principales con iconos.
- Llamadas a la acción: "Registrarse" e "Iniciar sesión".
- Ejemplos de anuncios de alojamiento destacados (sin autenticación).
- Sección de profesionales disponibles.
- Pie de página con información del proyecto.

**Acceso:** Público (sin autenticación).

---

### 10.2 Registro (`/register/`)

Formulario de creación de cuenta. Campos:
- Nombre y apellidos
- Correo electrónico
- Contraseña y confirmación
- Selección de rol (estudiante, abogado, orientador, propietario)
- Ciudad de residencia

Tras el registro, el usuario es redirigido al panel o al listado de anuncios según su rol.

**Acceso:** Solo usuarios no autenticados.

---

### 10.3 Inicio de sesión (`/login/`)

Formulario de autenticación con email y contraseña. Incluye enlace a la página de registro.

**Acceso:** Solo usuarios no autenticados.

---

### 10.4 Listado de anuncios de alojamiento (`/alojamiento/`)

Página principal del módulo de alojamiento:
- Barra de filtros (ciudad, tipo, precio máximo).
- Cuadrícula de tarjetas de anuncios aprobados.
- Cada tarjeta muestra: foto principal, título, ciudad, tipo, precio y botón "Ver detalle".
- Paginación si el número de anuncios es elevado.

**Acceso:** Usuarios autenticados.

---

### 10.5 Detalle de anuncio (`/alojamiento/<id>/`)

Página de detalle de un anuncio:
- Galería de fotos (foto principal + imágenes adicionales).
- Título, descripción completa, tipo, precio y ciudad.
- Datos del propietario (nombre, foto, ciudad).
- Botón "Contactar al propietario" → redirige al chat privado.
- Botón "Denunciar anuncio".

**Acceso:** Usuarios autenticados.

---

### 10.6 Formulario de creación de anuncio (`/alojamiento/crear/`)

Formulario para propietarios:
- Título, descripción, tipo, precio, ciudad.
- Carga de foto principal.
- Carga de imágenes adicionales (galería).
- Botón "Publicar" → anuncio queda pendiente de validación.

**Acceso:** Usuarios con rol `housing` o `admin`.

---

### 10.7 Directorio de profesionales (`/abogados/` y `/orientadores/`)

Listado de profesionales validados:
- Cuadrícula de fichas con foto, nombre, especialidad e idiomas.
- Filtro por ciudad.
- Botón "Ver ficha completa".

**Acceso:** Usuarios autenticados.

---

### 10.8 Ficha de profesional (`/profesional/<id>/`)

Página de detalle de un profesional:
- Foto, nombre, especialidad, idiomas, ciudad.
- Descripción bio.
- Botón "Enviar mensaje" → redirige al chat privado.
- Enlace al sitio web o LinkedIn (si disponible).

**Acceso:** Usuarios autenticados.

---

### 10.9 Chat privado (`/chat/privado/<user_id>/`)

Interfaz de mensajería privada:
- Área de mensajes con scroll (mensajes propios a la derecha, del interlocutor a la izquierda).
- Burbuja con nombre, foto y mensaje.
- Campo de texto + botón de envío.
- Los mensajes se actualizan en tiempo real vía WebSocket.

**Acceso:** Usuarios autenticados.

---

### 10.10 Chat de grupo (`/chat/grupo/<id>/`)

Interfaz de chat grupal:
- Nombre del grupo y ciudad en el encabezado.
- Lista de miembros conectados (barra lateral).
- Área de mensajes en tiempo real.
- Campo de texto + envío vía WebSocket.

**Acceso:** Usuarios autenticados que pertenecen al grupo.

---

### 10.11 Panel de administración (`/dashboard/`)

Dashboard exclusivo para administradores:
- Tarjetas de estadísticas: usuarios totales, anuncios pendientes, denuncias abiertas.
- Tabla de últimas acciones (ActivityLog).
- Menú lateral con acceso a: usuarios, anuncios, denuncias y grupos.
- Acciones rápidas de moderación desde cada tabla.

**Acceso:** Exclusivo para rol `admin`.

---

### 10.12 Perfil de usuario (`/perfil/`)

Página de perfil propio:
- Foto de perfil, nombre, email, ciudad, teléfono.
- Rol actual del usuario.
- Botón "Editar perfil".
- Para profesionales: resumen de su ficha profesional.
- Para propietarios: enlace a "Mis anuncios".

**Acceso:** Usuarios autenticados (solo su propio perfil).
