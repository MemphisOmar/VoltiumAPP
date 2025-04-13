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
        page.dialog.open = False  # Close the current dialog first
        page.update()
        
        page.dialog = ft.AlertDialog(
            modal=True,  # Make dialog modal
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
        modal=True,  # Make dialog modal
        title=ft.Text("Ayuda del juego", size=24, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                ft.Text("¿Qué tipo de ayuda necesita?", size=20, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.TextButton("Código de Colores", on_click=mostrar_codigo_colores),
                    ft.TextButton("Video Explicativo", on_click=abrir_explicacion)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=colors.GREY_300
    )
    page.dialog.open = True
    page.update()