import flet as ft
import os
import sys
import json

# Asegurar que el directorio actual está en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from juego import configurar_ventana_juego  #Importar la subrutina desde juego.py
from login import mostrar_formulario_perfil
from ayuda import mostrar_ayuda

PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_profile.json")


def main(page: ft.Page):
    # Variable de control para el estado de la aplicación
    page.app_running = True

    def cargar_perfil():
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def mostrar_formulario_perfil_app():
        def on_perfil_guardado(perfil):
            page.clean()
            mostrar_menu()
            page.update()
        mostrar_formulario_perfil(page, on_perfil_guardado)

    def mostrar_menu():
        def jugar_click(e):
            if page.app_running:
                page.clean()
                configurar_ventana_juego(page, main)
                page.update()

        def ayuda_click(e):
            if page.app_running:
                page.update()
                mostrar_ayuda(page)
                page.update()

        def salir_click(e):
            page.app_running = False
            page.window.close()

        jugar_button = ft.ElevatedButton(text="JUGAR", on_click=jugar_click, width=200, height=50, color="#29c589")
        ayuda_button = ft.ElevatedButton(text="AYUDA", on_click=ayuda_click, width=200, height=50, color="#29c589")
        salir_button = ft.ElevatedButton(text="SALIR", on_click=salir_click, width=200, height=50, color="#29c589")

        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="MAIN/Voltium_LOGO2.png")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                ),
                expand=True,
                alignment=ft.alignment.top_center,  
                width=1024,
                height=768
            )
        )

        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        jugar_button,
                        ayuda_button,
                        salir_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                ),
                expand=True,
                alignment=ft.alignment.bottom_center, 
                width=800,
                height=900,
            )
        )
        page.update()

    def on_window_event(e):
        if e.data == "close":
            page.app_running = False
            page.window_destroy()

    page.window.on_event = on_window_event
    page.clean()
    page.title = "VOLTIUM"
    page.bgcolor = "#88B98A"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 720
    page.window.height = 1280
    page.window.resizable = False
    page.padding = 0
    page.margin = 0

    perfil = cargar_perfil()
    if perfil is None:
        mostrar_formulario_perfil_app()
    else:
        mostrar_menu()

if __name__ == "__main__":
    ft.app(target=main)


