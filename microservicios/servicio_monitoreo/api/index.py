import os
import sys

# Permite importar app.py, config.py, etc. desde la carpeta del servicio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402,F401  (Vercel busca la variable "app")
