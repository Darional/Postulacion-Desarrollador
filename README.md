# Prueba Técnica FastAPI + MongoDB

## Introducción

Este proyecto es una API REST desarrollada en **FastAPI**, usando **MongoDB** como base de datos. Se encuentra dockerizado para facilitar su despliegue y uso.

---

## Requisitos previos

- **Git**
- **Docker**
- (**Opcional, recomendado**) Docker Desktop para comodidad visual.

---

## Instalación y ejecución

1. **Clona el repositorio**:

```bash
git clone https://github.com/Darional/Postulacion-Desarrollador.git
cd Postulacion-Desarrollador
```

2. **Ejecuta Docker Compose** para levantar los servicios:

```bash
docker compose up --build
```

Esto iniciará dos contenedores:

- **fastapi**: API REST (puerto `8000`)
- **mongo**: Base de datos MongoDB (puerto `27017`)

---

## Probar las funcionalidades (Swagger UI)

Accede desde tu navegador a:

```
http://localhost:8000/docs
```

Hay una interfaz visual interactiva para probar los endpoints disponibles, incluyendo:

- **Registro de usuario (`/register`)**
- Validaciones integradas (email único, formato correcto, complejidad de contraseña, etc.)

La interfaz acepta datos en formato JSON directamente.

---

## Ejecutar tests unitarios (pytest)

El proyecto incluye tests automáticos implementados con **pytest**, cubriendo:

- Registro correcto de un usuario nuevo.
- Validación de correo electrónico duplicado.
- Validación de correo electrónico mal formado.
- Validación de complejidad mínima de la contraseña.

Para ejecutarlos:

**Opción A (Docker Desktop)**:

1. Abre Docker Desktop.
2. Selecciona el contenedor **fastapi** → **Terminal (exec)**.
3. Ejecuta:
```bash
pytest -q
```

**Opción B (línea de comandos)**:

Ejecuta en tu terminal (reemplaza el nombre del contenedor si es distinto):

```bash
docker exec -it postulacion-desarrollador-fastapi-1 /bin/sh
pytest -q
```

---


## Variables de entorno (.env)

El archivo `.env` se usa para configurar variables sensibles (URLs), proximamente se eliminará del repositorio. Un ejemplo es:

```bash
DATABASE_URL=mongodb://mongo:27017/DBPruebaTecnica
```

Puedes modificarlo según necesidades específicas de tu entorno.

---

## Notas adicionales

- El proyecto usa contraseñas hasheadas con bcrypt y tokens JWT con clave secreta.
- La base de datos es persistente solo mientras los contenedores están arriba (a menos que añadas volúmenes permanentes en Docker Compose).

---

## Autor

- **Darael Badilla** - [badilladarael@gmail.com](mailto:badilladarael@gmail.com)

