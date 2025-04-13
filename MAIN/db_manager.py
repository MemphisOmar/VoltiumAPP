import sqlite3
import os
import random

class DBManager:
    def __init__(self):
        self.db_path = "jugadores.db"
        self.crear_base_datos()

    def crear_base_datos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='jugadores' ''')
        
        if cursor.fetchone()[0] == 0:
            # Table doesn't exist, create it with all columns
            cursor.execute('''
                CREATE TABLE jugadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    grupo TEXT NOT NULL,
                    puntaje INTEGER NOT NULL,
                    tiempo INTEGER,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        else:
            # Table exists, check if tiempo column exists
            cursor.execute('PRAGMA table_info(jugadores)')
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'tiempo' not in columns:
                # Add tiempo column if it doesn't exist
                cursor.execute('ALTER TABLE jugadores ADD COLUMN tiempo INTEGER')
        
        conn.commit()
        conn.close()

    def registrar_jugador(self, nombre, grupo):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generar puntaje aleatorio entre 70 y 100
        puntaje = random.randint(70, 100)
        
        cursor.execute('''
            INSERT INTO jugadores (nombre, grupo, puntaje)
            VALUES (?, ?, ?)
        ''', (nombre, grupo, puntaje))
        
        conn.commit()
        conn.close()
        return puntaje

    def obtener_ultimos_puntajes(self, limite=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT nombre, grupo, puntaje, fecha
            FROM jugadores
            ORDER BY fecha DESC
            LIMIT ?
        ''', (limite,))
        
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def actualizar_puntaje(self, nombre, grupo, puntaje, tiempo):
        """
        Guarda o actualiza el puntaje de un jugador
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO jugadores (nombre, grupo, puntaje, tiempo)
                VALUES (?, ?, ?, ?)
            ''', (nombre, grupo, puntaje, tiempo))
            conn.commit()
        except sqlite3.OperationalError:
            # If insert fails, try without tiempo column
            cursor.execute('''
                INSERT INTO jugadores (nombre, grupo, puntaje)
                VALUES (?, ?, ?)
            ''', (nombre, grupo, puntaje))
            conn.commit()
        finally:
            conn.close()
