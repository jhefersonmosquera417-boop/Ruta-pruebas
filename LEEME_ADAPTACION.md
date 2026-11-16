# Adaptación a Supabase (PostgreSQL) + Vercel

Copia estos archivos dentro de tu proyecto, respetando las carpetas y
reemplazando los que ya existan.

## Qué cambia
| Archivo | Cambio |
|---|---|
| `microservicios/*/database.py` | `pymysql` -> `psycopg2` (conexión con SSL) |
| `microservicios/servicio_rutas/repository.py` | `LIKE` -> `unaccent(...) ILIKE unaccent(...)` (ignora mayúsculas y tildes como MySQL) |
| `microservicios/servicio_monitoreo/repository.py` | igual que arriba + `RETURNING id` en lugar de `lastrowid` + booleano real |
| `microservicios/servicio_rutas/models.py`, `servicio_operaciones/models.py` | se quita `spyne` (clases equivalentes, mismo uso) |
| `microservicios/*/api/index.py`, `vercel.json`, `requirements.txt` | NUEVOS: punto de entrada y configuración para Vercel |
| `base_de_datos/esquema_postgres.sql` | NUEVO: esquema para el SQL Editor de Supabase |
| `base_de_datos/conexion_bd.py` | versión PostgreSQL |
| `frontend/vercel.json` | NUEVO: evita el 404 al recargar rutas de vue-router |
| `requirements.txt` (raíz), `.env.example` | PyMySQL -> psycopg2-binary; variables nuevas |

## Variables de entorno en Vercel (los 3 backends)
DB_HOST, DB_USER, DB_PASSWORD, DB_NAME (postgres), DB_PORT (6543),
JWT_SECRET_KEY y API_KEY (iguales en los tres).
