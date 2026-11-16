import os
import sys

# Carpeta de este microservicio dentro del repositorio
_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_RAIZ, "microservicios", "servicio_monitoreo"))

from app import app  # noqa: E402  (Vercel busca la variable "app")


class _QuitarPrefijo:
    """Vercel entrega la ruta completa (/api/monitoreo/...). Se quita el prefijo
    para que las rutas originales del servicio funcionen sin cambios."""

    def __init__(self, wsgi_app, prefijo):
        self.wsgi_app = wsgi_app
        self.prefijo = prefijo

    def __call__(self, environ, start_response):
        ruta = environ.get("PATH_INFO", "")
        if ruta.startswith(self.prefijo):
            environ["PATH_INFO"] = ruta[len(self.prefijo):] or "/"
        return self.wsgi_app(environ, start_response)


app.wsgi_app = _QuitarPrefijo(app.wsgi_app, "/api/monitoreo")
