import sqlite3
import os

class DBManager:
    def __init__(self):
        self.db_path = "voltium.db"
        self.crear_base_datos()

    def crear_base_datos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Crear tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE,
                edad TEXT,
                sexo TEXT,
                carrera TEXT,
                grupo TEXT
            )
        ''')
        # Crear tabla de sesiones de juego relacionada al usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                sesiones INTEGER DEFAULT 0,
                tiempo TEXT DEFAULT "0:00:00",
                partidas INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        # Crear tabla de partidas individuales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partida (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                numero_partida INTEGER NOT NULL,
                tiempo TEXT DEFAULT "0:00:00",
                estado TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def registrar_usuario(self, user_id, edad, sexo, carrera, grupo):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (user_id, edad, sexo, carrera, grupo)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, edad, sexo, carrera, grupo))
            conn.commit()
            user_id = cursor.lastrowid  # Get the newly inserted user ID
            print(f"Usuario registrado con ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError as e:
            print(f"Error al registrar usuario: {e}")
            return None
        finally:
            conn.close()

    def obtener_info_usuario(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, edad, sexo, carrera, grupo
            FROM users
            WHERE id = ?
        ''', (user_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
