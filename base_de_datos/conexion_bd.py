# -*- coding: utf-8 -*-
"""
==============================================================================
MÓDULO: CONEXIÓN A BASE DE DATOS (PostgreSQL / Supabase)
==============================================================================
Gestiona la conexión centralizada a la base de datos PostgreSQL en Supabase.
"""

import os
from contextlib import contextmanager
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "sslmode": os.getenv("DB_SSLMODE", "require"),
    "connect_timeout": 10,
}

def get_db_connection():
    """Establece y retorna una conexión activa a PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

@contextmanager
def get_cursor(commit: bool = False):
    """
    Context manager seguro: abre conexión y cursor (filas como diccionario),
    realiza commit o rollback según corresponda y garantiza el cierre.
    """
    conn = get_db_connection()
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
