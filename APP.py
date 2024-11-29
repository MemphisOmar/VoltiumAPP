import flet as ft
from ayuda import mostrar_ayuda  #Importar la subrutina desde ayuda.py
from juego import configurar_ventana_juego  #Importar la subrutina desde juego.py

from flet import (
    Page,
    colors
)

def main(page: ft.Page):
    page.clean()  #Limpiar la página actual antes de agregar los elementos del menú
    page.title = "VOLTIUM"
    page.bgcolor = "#b9b3a7"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800  #Ancho de la ventana
    page.window_height = 900  #Alto de la ventana

    def jugar_click(e):
        configurar_ventana_juego(page, main)

    def ayuda_click(e):
        mostrar_ayuda(page)  #Llamar a la subrutina desde ayuda.py

    def salir_click(e):
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
            height=900
        )
    )



    page.update()  # Actualizar la página para reflejar los cambios

ft.app(target=main)