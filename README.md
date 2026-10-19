# API Gestión de Reservas - UCN

## Descripción
Plataforma backend desarrollada para gestionar la reserva de espacios físicos de la institución, solucionando problemas como reservas duplicadas, dificultad para conocer la disponibilidad, información desactualizada, dificultad para identificar quién realizó una reserva y ausencia de un historial centralizado. Construida mediante una API REST con FastAPI, SQLAlchemy, Alembic y SQLite.

## Instalación
1. Clonar el repositorio:
```bash
git clone <https://github.com/nachrojas/reservas-ucn.git>
cd reservas-ucn
```
2. Crear y activar el entorno virtual:
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```
3. Instalar las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

## Base de datos (Migraciones con Alembic)
La estructura de la base de datos se gestiona mediante Alembic bajo el enfoque Code-First. Para aplicar las migraciones y generar la base de datos `reservas.db`, ejecuta:
```bash
alembic upgrade head
```

## Datos Iniciales (Seeders)
El proyecto incluye un script reproducible para poblar la base de datos con 5 usuarios, 10 espacios y 15 reservas iniciales:
```bash
python seed.py
```

## Ejecución
Para iniciar el servidor de desarrollo con recarga automática:
```bash
uvicorn app.main:app --reload
```
* **Swagger UI (Documentación interactiva):** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

## Arquitectura por Capas
El proyecto implementa una arquitectura limpia separando responsabilidades:
* **Models (`app/models/`):** Entidades ORM de SQLAlchemy (`Usuario`, `Espacio`, `Reserva`) que representan las tablas y relaciones (`relationship`, `ForeignKey`) en la base de datos.
* **DTO / Schemas (`app/schemas/`):** Modelos Pydantic para validar datos de entrada y estructurar respuestas JSON, evitando exponer directamente los modelos SQLAlchemy y previniendo referencias circulares.
* **Repository (`app/repositories/`):** Encapsula todas las consultas SQLAlchemy (`select`, `add`, `commit`, `delete`). Ningún Router accede directamente a la base de datos.
* **Service (`app/services/`):** Contiene la lógica y reglas de negocio, incluyendo la validación que impide reservar un espacio en horarios superpuestos y el manejo de errores de dominio.
* **Router / Endpoints (`app/routers/`):** Controladores HTTP que reciben las peticiones, extraen parámetros (`Path`, `Query`, `Body`) y delegan la operación al Service correspondiente.
* **Database (`app/database.py`):** Configuración del motor SQLite (`engine`), fábrica de sesiones (`SessionLocal`) y clase base declarativa (`Base`).
* **Dependencies:** Uso de `Depends()` de FastAPI para inyectar la sesión de base de datos con manejo de ciclo de vida (`yield` / `close()`) hacia los repositorios y servicios.
* **Middleware (`app/main.py`):** Interceptor HTTP transversal que mide el tiempo de ejecución de cada request, inyecta el header `X-Process-Time` y registra en consola el método, ruta y código de estado.

## Aplicación de Principios SOLID
1. **Single Responsibility Principle (SRP):** Aplicado en la separación estricta entre `routers` (manejo HTTP), `services` (reglas de negocio como cruce de horarios) y `repositories` (persistencia SQLAlchemy). Cada clase tiene una única razón para cambiar.
2. **Open/Closed Principle (OCP):** Aplicado en el diseño de esquemas Pydantic (`esquemas.py`) y repositorios, donde las clases base (`UsuarioBase`, `EspacioBase`, `ReservaBase`) se extienden mediante herencia para crear esquemas específicos de creación, actualización parcial (`PATCH`) y respuesta sin modificar la estructura base.
3. **Dependency Inversion Principle (DIP):** Aplicado mediante la inyección de dependencias de FastAPI (`Depends`) e interfaces abstractas (`ABC`) en la capa de repositorios, permitiendo que los módulos de alto nivel (`Services` y `Routers`) dependan de abstracciones inyectadas y no instancien conexiones concretas directamente.

## Diferencia entre PUT y PATCH
* **`PUT`** (`/api/usuarios/{id}`, `/api/espacios/{id}`): Reemplaza el recurso por completo; requiere enviar todos los campos obligatorios del DTO. Es idempotente.
* **`PATCH`** (`/api/reservas/{id}`): Realiza una modificación parcial sobre el recurso usando `exclude_unset=True`, sin exigir el resto de los atributos.

## Tabla de Endpoints

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| **GET** | `/` | Comprueba el estado de funcionamiento de la API. |
| **GET** | `/api/usuarios` | Lista usuarios de forma paginada (`?page=1&limit=10`). |
| **GET** | `/api/usuarios/{id}` | Obtiene el detalle de un usuario por su ID. |
| **POST** | `/api/usuarios` | Crea un nuevo usuario (`201 Created`). |
| **PUT** | `/api/usuarios/{id}` | Reemplaza completamente los datos de un usuario existente. |
| **DELETE** | `/api/usuarios/{id}` | Elimina un usuario por su ID. |
| **GET** | `/api/espacios` | Lista espacios con paginación (`page`, `limit`) y filtros por `capacidad` y `disponible`. |
| **GET** | `/api/espacios/{id}` | Obtiene un espacio específico por su ID. |
| **POST** | `/api/espacios` | Crea un nuevo espacio físico (`201 Created`). |
| **PUT** | `/api/espacios/{id}` | Reemplaza todos los datos de un espacio existente. |
| **DELETE** | `/api/espacios/{id}` | Elimina un espacio físico del sistema. |
| **GET** | `/api/reservas` | Lista reservas paginadas (`page`, `limit`) permitiendo filtrar por `usuario`, `espacio`, `fecha` y `estado`. |
| **GET** | `/api/reservas/{id}` | Obtiene el detalle de una reserva específica por su ID. |
| **POST** | `/api/reservas` | Crea una reserva validando que no exista superposición de horarios (`201 Created`). |
| **PATCH** | `/api/reservas/{id}` | Actualiza parcialmente una reserva (ej. cambiar `estado` a `cancelada`) validando disponibilidad horaria. |
| **DELETE** | `/api/reservas/{id}` | Elimina o cancela una reserva existente por su ID. |  