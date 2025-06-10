import sqlite3
import os

class SesionManager:
    def __init__(self, user_id, db_path="voltium.db"):
        self.db_path = db_path
        self.user_id = user_id
        self.crear_registro_usuario()

    def crear_registro_usuario(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Asegurarse de que haya un registro de sesión para el usuario
        cursor.execute('SELECT COUNT(*) FROM sesion WHERE user_id = ?', (self.user_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO sesion (user_id, sesiones, tiempo, partidas) VALUES (?, 0, 0, 0)', (self.user_id,))
        conn.commit()
        conn.close()

    def incrementar_sesion(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE sesion SET sesiones = sesiones + 1 WHERE user_id = ?', (self.user_id,))
        conn.commit()
        conn.close()

    def incrementar_tiempo(self, minutos):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE sesion SET tiempo = tiempo + ? WHERE user_id = ?', (minutos, self.user_id))
        conn.commit()
        conn.close()

    def incrementar_partidas(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE sesion SET partidas = partidas + 1 WHERE user_id = ?', (self.user_id,))
        conn.commit()
        conn.close()

    def obtener_datos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT sesiones, tiempo, partidas FROM sesion WHERE user_id = ?', (self.user_id,))
        datos = cursor.fetchone()
        conn.close()
        return {
            'sesiones': datos[0] if datos else 0,
            'tiempo': datos[1] if datos else 0,
            'partidas': datos[2] if datos else 0
        }
