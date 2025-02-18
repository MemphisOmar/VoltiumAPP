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
        
        # Crear tabla de jugadores si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                grupo TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
