import os
import random
import sys
from faker import Faker
from faker.providers import lorem, file, person, company,profile
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Agregar el directorio raíz al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import create_connection, close_connection
from utils.poblar_usuarios import poblar_usuarios_institucionales

# Configuración de Faker
fake = Faker('es_ES')
fake.add_provider(lorem)
fake.add_provider(file)
fake.add_provider(person)
fake.add_provider(company)
fake.add_provider(profile)

# Cargar variables de entorno
load_dotenv()

def obtener_usuarios(cursor):
    """Obtiene la lista de IDs de usuarios existentes"""
    try:
        cursor.execute("SELECT id_usuario FROM usuario")
        usuarios = [usuario[0] for usuario in cursor.fetchall()]
        return usuarios
    except mysql.connector.Error as err:
        print(f"❌ Error al obtener usuarios: {err}")
        return []

generar_documento = lambda: f"documento_{fake.uuid4()}.pdf"

def generar_registro_historico(id_usuario=None):
    """Genera un diccionario con datos ficticios para un registro histórico"""
    tipos_documento = ['acta_nacimiento', 'acta_matrimonio', 'acta_defuncion', 'titulo_academico', 'otra']
    fuentes = ['Registro Civil', 'Notaría', 'Universidad', 'Ministerio de Salud', 'Archivo Nacional', None]
    
    # Generar fechas aleatorias en los últimos 5 años
    fecha_subida = fake.date_time_between(start_date='-5y', end_date='now')
    
    # Generar datos ficticios
    registro = {
        'descripcion': fake.paragraph(nb_sentences=3),
        'tipo_documento': random.choice(tipos_documento),
        'url_documento': generar_documento(),
        'id_usuario_subida': id_usuario,
        'fecha_subida': fecha_subida.strftime('%Y-%m-%d %H:%M:%S'),
        'fuente_validadora': random.choice(fuentes)
    }
    
    # Ajustar la descripción según el tipo de documento
    if registro['tipo_documento'] == 'acta_nacimiento':
        registro['descripcion'] = f"Acta de nacimiento de {fake.name()}, emitida en {fake.city()}"
    elif registro['tipo_documento'] == 'acta_matrimonio':
        registro['descripcion'] = f"Acta de matrimonio entre {fake.name()} y {fake.name()}, celebrado en {fake.city()}"
    elif registro['tipo_documento'] == 'acta_defuncion':
        registro['descripcion'] = f"Acta de defunción de {fake.name()}, registrada en {fake.city()}"
    elif registro['tipo_documento'] == 'titulo_academico':
        registro['descripcion'] = f"Título académico en {fake.job()} emitido por {fake.company()}"
    
    return registro

def insertar_registros_historicos(cantidad=10):
    """Inserta registros históricos ficticios en la base de datos"""
    conn = create_connection()
    if not conn:
        print("No se pudo conectar a la base de datos. Verifica la configuración en el archivo .env")
        print("Asegúrate de que las siguientes variables estén configuradas:")
        print("HOSTNAME, DB_PORT, USERNAME, PASSWORD, DATABASE")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Asegurar que existan usuarios institucionales
        print("\n🔍 Verificando usuarios existentes...")
        usuarios = obtener_usuarios(cursor)
        
        if not usuarios:
            print("ℹ️  No se encontraron usuarios existentes. Creando usuarios institucionales...")
            if not poblar_usuarios_institucionales(3):
                print("❌ No se pudieron crear usuarios institucionales")
                return False
            
            # Obtener los usuarios recién creados
            usuarios = obtener_usuarios(cursor)
        
        print(f"✅ Usuarios disponibles: {len(usuarios)}")
        
        if not usuarios:
            print("❌ No hay usuarios disponibles para asignar a los registros")
            return False
    
        # Insertar registros
        for i in range(cantidad):
            # Seleccionar un usuario aleatorio (siempre debe haber al menos uno)
            id_usuario = random.choice(usuarios)
            
            # Generar registro histórico
            registro = generar_registro_historico(id_usuario)
            
            # Insertar en la base de datos
            query = """
            INSERT INTO registro_historico 
            (descripcion, tipo_documento, url_documento, id_usuario_subida, fecha_subida, fuente_validadora)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                registro['descripcion'],
                registro['tipo_documento'],
                registro['url_documento'],
                registro['id_usuario_subida'],
                registro['fecha_subida'],
                registro['fuente_validadora']
            ))
            
            # Mostrar progreso cada 10 registros
            if (i + 1) % 10 == 0:
                print(f"Progreso: {i + 1}/{cantidad} registros creados")
        
        conn.commit()
        print(f"\nSe han insertado {cantidad} registros históricos correctamente.")
        return True
        
    except mysql.connector.Error as err:
        print(f"\nError al insertar registros históricos: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_connection(conn)

def obtener_cantidad():
    """Pide al usuario la cantidad de registros a generar"""
    while True:
        try:
            entrada = input("¿Cuántos registros históricos desea generar? (por defecto 20): ").strip()
            if not entrada:
                return 20
            cantidad = int(entrada)
            if cantidad > 0:
                return cantidad
            print("Por favor ingrese un número mayor a 0.")
        except ValueError:
            print("Por favor ingrese un número válido.")

if __name__ == "__main__":
    print("=" * 50)
    print("  GENERADOR DE REGISTROS HISTÓRICOS")
    print("=" * 50)
    
    cantidad = obtener_cantidad()
    insertar_registros_historicos(cantidad)
    print("\n✨ Proceso completado")
