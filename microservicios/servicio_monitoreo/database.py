import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from config import Config


def _get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dbname=Config.DB_NAME,
        port=Config.DB_PORT,
        sslmode=os.getenv("DB_SSLMODE", "require"),  # Supabase exige SSL
        connect_timeout=10,
    )


@contextmanager
def get_cursor(commit: bool = False):
    """
    Context manager: abre conexión y cursor, y garantiza el cierre
    aunque ocurra una excepción (evita fugas de conexiones).
    'commit=True' se usa en operaciones de escritura (INSERT/UPDATE/DELETE).
    Las filas se devuelven como diccionarios (igual que DictCursor en MySQL).
    """
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            yield cursor
            if commit:
                conn.commit()
    except Exception:
        if commit:
            conn.rollback()
        raise
    finally:
        conn.close()
