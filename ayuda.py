import flet as ft
import webbrowser

from flet import (
    Page,
    colors
)

def mostrar_ayuda(page: ft.Page):
    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    def mostrar_codigo_colores(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Código de Colores"),
            content=ft.Image(src="Resistencia.png", fit=ft.ImageFit.CONTAIN),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_dialogo)
            ],
            bgcolor=colors.GREY_300
        )
        page.dialog.open = True
        page.update()

    def abrir_explicacion(e):
        webbrowser.open("https://www.youtube.com/shorts/nbPFl_Icn78")

    page.dialog = ft.AlertDialog(
        title=ft.Text("Ayuda del juego"),
        content=ft.Text("Sería usted tan amable de seleccionar la ayuda que", size=20),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo),
            ft.TextButton("Código de Colores", on_click=mostrar_codigo_colores),
            ft.TextButton("EXPLICACION", on_click=abrir_explicacion)
        ]
    )
    page.dialog.open = True
    page.update()