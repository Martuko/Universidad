import psycopg2
import os

def obtener_conexion():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        DATABASE_URL = 'postgres://u704a5ln8sar5c:pb91fd1049f61702a300d7ed31f7984963e5837e9788c2febf90465f105ef05a3@ce0lkuo944ch99.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4ra8hg5s8stsv'
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn
