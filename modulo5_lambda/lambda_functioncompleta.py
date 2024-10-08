import gspread
from google.oauth2.service_account import Credentials
import psycopg2
import os

def lambda_handler(event, context):
    # Configuración de Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('unisabana-cloud-99b5a09fc655.json', scopes=scope)
    client = gspread.authorize(creds)
    
    # Abrir la hoja de cálculo
    sheet = client.open('2024_AWS_LAMBDA').sheet1

    data = sheet.get_all_records()

    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    cur = conn.cursor()

    # Insertar datos en PostgreSQL
    for row in data:
        cur.execute("""
            INSERT INTO notas_clase (id, nombre_estudiante, nota)
            VALUES (%s, %s, %s)
        """, (row['id'], row['nombre_estudiante'], row['nota']))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': 'Datos insertados correctamente'
    }