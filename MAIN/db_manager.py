import requests

SUPABASE_URL = "https://esvonxxkcujuaaxifjsw.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzdm9ueHhrY3VqdWFheGlmanN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExMjgwNjgsImV4cCI6MjA2NjcwNDA2OH0.VTvzI7S1qs8kUjk4AYiTl0iSL1EQ3YT9AJF3swT8gT0"
SUPABASE_HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

class DBManager:
    def __init__(self):
        pass  # No local DB setup needed

    def insert(self, table, data):
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        headers = SUPABASE_HEADERS.copy()
        headers["Prefer"] = "return=representation"
        response = requests.post(url, headers=headers, json=data)
        try:
            return response.json()
        except Exception:
            print("Respuesta no JSON:", response.text)
            return None

    def select(self, table, filters=None):
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        params = {"select": "*"}
        if filters:
            params.update(filters)
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        try:
            return response.json()
        except Exception:
            print("Respuesta no JSON:", response.text)
            return None

    def update(self, table, filters, data):
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=filters, json=data)
        try:
            return response.json()
        except Exception:
            print("Respuesta no JSON:", response.text)
            return None

    def delete(self, table, filters):
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        response = requests.delete(url, headers=SUPABASE_HEADERS, params=filters)
        try:
            return response.json()
        except Exception:
            print("Respuesta no JSON:", response.text)
            return None

    def registrar_usuario(self, user_id, edad, sexo, carrera, grupo):
        data = {
            "user_id": user_id,
            "edad": edad,
            "sexo": sexo,
            "carrera": carrera,
            "grupo": grupo
        }
        result = self.insert("USERS", data)
        # Mostrar el error si la inserción falla
        if isinstance(result, dict) and result.get('message'):
            print("Error Supabase:", result['message'])
        if isinstance(result, list) and len(result) > 0 and "user_id" in result[0]:
            return result[0]["user_id"]
        return None

    def registrar_partida(self, user_id, numero_partida, tiempo, estado):
        data = {
            "user_id": user_id,
            "numero_partida": numero_partida,
            "tiempo": tiempo,
            "estado": estado
        }
        result = self.insert("partida", data)
        if isinstance(result, dict) and result.get('message'):
            print("Error Supabase partida:", result['message'])
        return result

    def registrar_sesion(self, user_id, sesiones, tiempo, partidas):
        data = {
            "user_id": user_id,
            "sesiones": sesiones,
            "tiempo": tiempo,
            "partidas": partidas
        }
        result = self.insert("sesion", data)
        if isinstance(result, dict) and result.get('message'):
            print("Error Supabase sesion:", result['message'])
        return result

# Ejemplo de uso:
# db = DBManager()
# db.insert("usuarios", {"nombre": "Juan", "email": "juan@ejemplo.com"})
# db.select("usuarios", {"nombre": "eq.Juan"})
# db.update("usuarios", {"id": "eq.1"}, {"nombre": "Juan Actualizado"})
# db.delete("usuarios", {"id": "eq.1"})
