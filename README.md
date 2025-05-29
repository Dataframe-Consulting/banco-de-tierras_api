# Banco de Tierras API

API REST para la gestión de un sistema de Banco de Tierras desarrollada con FastAPI, permitiendo administrar propiedades inmobiliarias y toda la información relacionada con ellas, incluyendo propietarios, ubicaciones, garantías, procesos legales y más.

## 🛠️ Instalación y configuración

1. **Clonar el repositorio**
```bash
git clone https://github.com/Dataframe-Consulting/banco-de-tierras_api
cd banco-de-tierras_api
```

2. **Verificar que Docker esté funcionando**
```bash
docker --version
docker-compose --version
```

3. **Levantar los servicios**
```bash
docker-compose up -d --build
```

4. **Comandos generales**
```bash
# Ver los logs para verificar que todo funciona
docker-compose logs -f

# Ver servicios en ejecución
docker-compose ps

# Detener los servicios
docker-compose down

# Ver logs de un servicio específico
docker-compose logs api
docker-compose logs db

# Ver qué hay en la base de datos
docker-compose exec db psql -U postgres -d postgres -c "\dt"

# Contar registros en una tabla (debería ser 0)
docker-compose exec db psql -U postgres -d postgres -c "SELECT COUNT(*) FROM propiedad;"
```

**Nota importante**: La API estará disponible en `http://localhost:8000` y la base de datos PostgreSQL en el puerto `5434`.

## 📚 Estructura de la API

### Endpoints Principales

#### 🟢 Endpoints públicos (sin autenticación)
- `GET /api/health` - Verificar estado de la API.
- `POST /api/auth/login` - Iniciar sesión.

#### 🔒 Endpoints protegidos (requieren autenticación)

**Autenticación**
- `GET /api/auth/me` - Obtener información del usuario actual.
- `POST /api/auth/logout` - Cerrar sesión.

**Propiedades**
- `GET /api/propiedad/` - Listar todas las propiedades.
- `GET /api/propiedad/{id}` - Obtener propiedad específica.
- `POST /api/propiedad/` - Crear nueva propiedad.
- `PUT /api/propiedad/{id}` - Actualizar propiedad.
- `DELETE /api/propiedad/{id}` - Eliminar propiedad.

**Relaciones de propiedades**
- `POST /api/propiedad/{id}/propietario/{propietario_id}/sociedad/{porcentaje}/es_socio/{bool}` - Agregar propietario.
- `DELETE /api/propiedad/{id}/propietario/{propietario_id}` - Remover propietario.
- `POST /api/propiedad/{id}/ubicacion/{ubicacion_id}` - Agregar ubicación.
- `POST /api/propiedad/{id}/garantia/{garantia_id}` - Agregar garantía.
- `POST /api/propiedad/{id}/proceso_legal/{proceso_id}` - Agregar proceso legal.

**Todos los módulos siguientes requieren autenticación:**
- **Propietarios**: `/api/propietario/` (GET, POST, PUT, DELETE).
- **Ubicaciones**: `/api/ubicacion/` (GET, POST, PUT, DELETE).
- **Garantías**: `/api/garantia/` (GET, POST, PUT, DELETE).
- **Procesos Legales**: `/api/proceso_legal/` (GET, POST, PUT, DELETE).
- **Proyectos**: `/api/proyecto/` (GET, POST, PUT, DELETE).
- **Vocaciones**: `/api/vocacion/` (GET, POST, PUT, DELETE).
- **Vocaciones específicas**: `/api/vocacion_especifica/` (GET, POST, PUT, DELETE).
- **Situación física**: `/api/situacion_fisica/` (GET, POST, PUT, DELETE).
- **Rentas**: `/api/renta/` (GET, POST, PUT, DELETE).
- **Archivos**: `/api/archivo/` (GET, POST, PUT, DELETE).
- **Auditoría**: `/api/auditoria/` (Solo GET para consultar cambios).

> **💡 Importante**: Excepto `/api/health` y `/api/auth/login`, **TODOS** los demás endpoints requieren que el usuario esté autenticado. El sistema usa cookies HTTP-only, por lo que debes incluir `credentials: 'include'` en todas las peticiones desde el frontend.

### Filtros y búsqueda

La API soporta filtros avanzados en el endpoint de propiedades:
- `q`: Búsqueda por nombre.
- `proyecto_id`: Filtrar por proyecto.
- `ubicacion_id`: Filtrar por ubicación.
- `garantia_id`: Filtrar por garantía.
- `proceso_legal_id`: Filtrar por proceso legal.

## 🗄️ Esquema de base de datos

La API maneja las siguientes entidades principales:

- **Propiedades**: Entidad central con información básica de la propiedad.
- **Propietarios**: Personas físicas o jurídicas que poseen propiedades.
- **Ubicaciones**: Información geográfica y administrativa.
- **Garantías**: Garantías asociadas a las propiedades.
- **Procesos legales**: Procedimientos legales en curso.
- **Proyectos**: Proyectos a los que pertenecen las propiedades.
- **Vocaciones**: Tipos de uso del suelo.
- **Rentas**: Información de arrendamientos.
- **Archivos**: Documentos digitales asociados.
- **Auditoría**: Registro de cambios realizados.

## 🔒 Seguridad

- **Autenticación JWT**: Tokens seguros para verificar identidad.
- **Cookies HTTP-only**: Protección contra ataques XSS.
- **CORS configurado**: Control de acceso desde diferentes dominios.
- **Validación de datos**: Esquemas Pydantic para validar entrada.
- **Autorización por endpoints**: Protección de recursos sensibles.

