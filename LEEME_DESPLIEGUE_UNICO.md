# Despliegue único en Vercel (frontend + 3 microservicios)

Un solo proyecto de Vercel con:
- Frontend (Vue/Vite) compilado desde `frontend/`
- 3 funciones Python: `api/ms_rutas.py`, `api/ms_operaciones.py`, `api/ms_monitoreo.py`

URLs finales (mismo dominio, sin CORS):
- `https://TU-PROYECTO.vercel.app/`                 -> frontend
- `https://TU-PROYECTO.vercel.app/api/rutas/...`        -> servicio_rutas
- `https://TU-PROYECTO.vercel.app/api/operaciones/...`  -> servicio_operaciones
- `https://TU-PROYECTO.vercel.app/api/monitoreo/...`    -> servicio_monitoreo (login, alertas, despacho)

Variables de entorno (una sola vez, en el proyecto):
DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, JWT_SECRET_KEY, API_KEY

Root Directory: dejar el de la raíz del repositorio (vacío).
