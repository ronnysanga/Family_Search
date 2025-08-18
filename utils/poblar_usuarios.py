"""
Script para poblar la base de datos con usuarios institucionales de ejemplo.
"""
import os
import sys
import random
import hashlib
from faker import Faker
from faker.providers import company, profile
import mysql.connector
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import create_connection, close_connection

fake = Faker('es_ES')
fake.add_provider(company)
fake.add_provider(profile)

load_dotenv()

def crear_usuario_institucional(conn, cursor):
    """Crea un usuario institucional ficticio"""
    dominios = [
        'gob.ec', 'registrocivil.gob.ec', 'msp.gob.ec', 'educacion.gob.ec',
        'university.edu.ec', 'hospital.com.ec', 'notaria.gov.ec', 'municipio.gob.ec'
    ]
    
    nombre_institucion = fake.company()
    dominio = random.choice(dominios)
    
    usuario_base = nombre_institucion.lower().replace(' ', '.')[:15]
    email = f"{usuario_base}@{dominio}"
    
    password = "password123"  
    
    try:
        cursor.execute(
            """
            INSERT INTO usuario (nombres, apellidos, email, password)
            VALUES (%s, %s, %s, %s)
            """,
            (f"Departamento de {fake.bs().title()}", 
             nombre_institucion, 
             email,
             password)
        )
        user_id = cursor.lastrowid
        conn.commit()
        print(f"✅ Creado usuario institucional: {email} (ID: {user_id}, Contraseña: {password})")
        return user_id
    except mysql.connector.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                print(f"ℹ️  Usuario ya existente: {email} (ID: {result[0]})")
                return result[0]
        print(f"❌ Error al crear usuario institucional: {e}")
        return None

def poblar_usuarios_institucionales(cantidad=3):
    """Crea la cantidad especificada de usuarios institucionales"""
    conn = create_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos. Verifica la configuración en el archivo .env")
        return False
    
    try:
        cursor = conn.cursor()
        print(f"\n🔹 Creando {cantidad} usuarios institucionales...")
        
        usuarios_creados = 0
        for _ in range(cantidad):
            if crear_usuario_institucional(conn, cursor):
                usuarios_creados += 1
        
        print(f"\n✅ Se crearon {usuarios_creados} usuarios institucionales correctamente.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            close_connection(conn)

def obtener_cantidad_usuarios():
    """Pide al usuario la cantidad de usuarios a generar"""
    while True:
        try:
            entrada = input("¿Cuántos usuarios institucionales desea generar? (por defecto 3): ").strip()
            if not entrada:
                return 3
            cantidad = int(entrada)
            if cantidad > 0:
                return cantidad
            print("Por favor ingrese un número mayor a 0.")
        except ValueError:
            print("Por favor ingrese un número válido.")

if __name__ == "__main__":
    print("=" * 50)
    print("  GENERADOR DE USUARIOS INSTITUCIONALES")
    print("=" * 50)
    
    cantidad = obtener_cantidad_usuarios()
    poblar_usuarios_institucionales(cantidad)
    print("\n✨ Proceso completado")
