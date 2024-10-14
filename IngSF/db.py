# db.py
import psycopg2
import os

def obtener_conexion():
    # Obtener la URL de la base de datos desde la variable de entorno
    DATABASE_URL = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn
