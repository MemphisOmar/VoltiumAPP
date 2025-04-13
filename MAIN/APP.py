import flet as ft
import os
import sys

# Asegurar que el directorio actual está en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ayuda import mostrar_ayuda  #Importar la subrutina desde ayuda.py
from juego import configurar_ventana_juego  #Importar la subrutina desde juego.py

from flet import (
    Page,
    colors
)

def main(page: ft.Page):
    # Variable de control para el estado de la aplicación
    page.app_running = True
    
    def on_window_event(e):
        if e.data == "close":
            page.app_running = False
            page.window_destroy()
    
    page.window.on_event = on_window_event
    
    page.clean()  #Limpiar la página actual antes de agregar los elementos del menú
    page.title = "VOLTIUM"
    page.bgcolor = "#88B98A"  # Color de fondo verde claro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 720
    page.window.height = 1280
    page.window.resizable = False
    page.padding = 0
    page.margin = 0

    def jugar_click(e):
        if page.app_running:
            page.clean()
            configurar_ventana_juego(page, main)
            page.update()

    def ayuda_click(e):
        if page.app_running:
            mostrar_ayuda(page)  # Removed page.clean() as it was clearing the main window
            page.update()

    def salir_click(e):
        page.app_running = False
        page.window_close()

    jugar_button = ft.ElevatedButton(text="JUGAR", on_click=jugar_click, width=200, height=50, color="#29c589")
    ayuda_button = ft.ElevatedButton(text="AYUDA", on_click=ayuda_click, width=200, height=50, color="#29c589")
    salir_button = ft.ElevatedButton(text="SALIR", on_click=salir_click, width=200, height=50, color="#29c589")

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="Voltium_LOGO2.png")
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


    page.update()  # Actualizar la página para reflejar los cambios

if __name__ == "__main__":
    ft.app(target=main)


