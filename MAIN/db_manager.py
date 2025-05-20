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

        # Crear tabla de sesiones de juego
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tiempo INTEGER,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
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

    def registrar_sesion_juego(self, user_id, tiempo):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO game_sessions (user_id, tiempo)
                VALUES (?, ?)
            ''', (user_id, tiempo))
            conn.commit()
            session_id = cursor.lastrowid
            print(f"Sesión de juego registrada con ID: {session_id}")
            return session_id
        except sqlite3.IntegrityError as e:
            print(f"Error al registrar sesión de juego: {e}")
            return None
        finally:
            conn.close()

    def obtener_sesiones_usuario(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT session_id, tiempo, fecha
            FROM game_sessions
            WHERE user_id = ?
        ''', (user_id,))
        resultados = cursor.fetchall()
        conn.close()
        return resultados

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
