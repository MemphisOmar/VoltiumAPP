import sqlite3
import os
from datetime import timedelta

def sumar_tiempos(t1, segundos):
    # t1 es un string 'HH:MM:SS', segundos es int
    h, m, s = [int(x) for x in t1.split(":")] if t1 else (0, 0, 0)
    total = timedelta(hours=h, minutes=m, seconds=s) + timedelta(seconds=segundos)
    return str(total)

class SesionManager:
    def __init__(self, user_id, db_path="voltium.db"):
        self.db_path = db_path
        self.user_id = user_id
        self.crear_registro_usuario()

    def crear_registro_usuario(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sesion WHERE user_id = ?', (self.user_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO sesion (user_id, sesiones, tiempo, partidas) VALUES (?, 0, "0:00:00", 0)', (self.user_id,))
        conn.commit()
        conn.close()

    def incrementar_sesion(self):
        from db_manager import DBManager
        db = DBManager()
        # Obtener datos actuales de la sesión
        filtro = {"user_id": f"eq.{self.user_id}"}
        sesiones_actuales = db.select("sesion", filtro)
        if sesiones_actuales and isinstance(sesiones_actuales, list) and len(sesiones_actuales) > 0:
            # Actualizar la fila existente
            db.actualizar_sesion(self.user_id, 1, "00:00:00", 0)
        else:
            # Crear nueva fila solo si no existe
            db.registrar_sesion(self.user_id, 1, "00:00:00", 0)

    def incrementar_tiempo(self, segundos):
        from db_manager import DBManager
        db = DBManager()
        # Obtener datos actuales de la sesión
        filtro = {"user_id": f"eq.{self.user_id}"}
        sesiones_actuales = db.select("sesion", filtro)
        h = segundos // 3600
        m = (segundos % 3600) // 60
        s = segundos % 60
        tiempo_str = f"{h:02d}:{m:02d}:{s:02d}"
        if sesiones_actuales and isinstance(sesiones_actuales, list) and len(sesiones_actuales) > 0:
            db.actualizar_sesion(self.user_id, 0, tiempo_str, 0)
        else:
            db.registrar_sesion(self.user_id, 0, tiempo_str, 0)

    def incrementar_partidas(self):
        from db_manager import DBManager
        db = DBManager()
        filtro = {"user_id": f"eq.{self.user_id}"}
        sesiones_actuales = db.select("sesion", filtro)
        if sesiones_actuales and isinstance(sesiones_actuales, list) and len(sesiones_actuales) > 0:
            db.actualizar_sesion(self.user_id, 0, "00:00:00", 1)
        else:
            db.registrar_sesion(self.user_id, 0, "00:00:00", 1)

    def obtener_datos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT sesiones, tiempo, partidas FROM sesion WHERE user_id = ?', (self.user_id,))
        datos = cursor.fetchone()
        conn.close()
        return {
            'sesiones': datos[0] if datos else 0,
            'tiempo': datos[1] if datos else "0:00:00",
            'partidas': datos[2] if datos else 0
        }

    def registrar_partida_individual(self, numero_partida, tiempo, estado):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO partida (user_id, numero_partida, tiempo, estado)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, numero_partida, tiempo, estado))
        conn.commit()
        conn.close()
