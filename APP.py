import flet as ft

from flet import (
    Page,
    colors
)


def main(page: ft.Page):
    page.title = "VOLTIUM"
    page.bgcolor = colors.PURPLE_500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800  # Ancho de la ventana
    page.window_height = 900  # Alto de la ventana

    def jugar_click(e):
        page.dialog = ft.AlertDialog(title=ft.Text("¡Comenzando el juego!"))
        page.dialog.open = True
        page.update()

    def ayuda_click(e):
        page.dialog = ft.AlertDialog(title=ft.Text("Ayuda del juego"))
        page.dialog.open = True
        page.update()

    def salir_click(e):
        page.window_close()

    jugar_button = ft.ElevatedButton(text="JUGAR", on_click=jugar_click, width=200, height=50, color=colors.LIGHT_GREEN_ACCENT_700)
    ayuda_button = ft.ElevatedButton(text="AYUDA", on_click=ayuda_click, width=200, height=50)
    salir_button = ft.ElevatedButton(text="SALIR", on_click=salir_click, width=200, height=50)

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
            image_src="R.png",  # Ruta de la imagen de fondo
            expand=True,
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main)