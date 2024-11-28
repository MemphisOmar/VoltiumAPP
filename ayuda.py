# ayuda.py
import flet as ft

def mostrar_ayuda(page: ft.Page):
    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    page.dialog = ft.AlertDialog(
        title=ft.Text("Ayuda del juego"),
        content=ft.Text("Aquí puedes poner la información de ayuda. AYUDA"),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo)
        ]
    )
    page.dialog.open = True
    page.update()