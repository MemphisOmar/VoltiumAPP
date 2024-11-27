import flet as ft

from flet import (
    Page,
    colors
)

def volver_al_menu_click(e):
    main(e.page)

def main(page: ft.Page):
    page.clean()  # Limpiar la página actual antes de agregar los elementos del menú
    page.title = "VOLTIUM"
    page.bgcolor = colors.PINK_ACCENT_200
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800  # Ancho de la ventana
    page.window_height = 900  # Alto de la ventana

    def jugar_click(e):
        configurar_ventana_juego(page)

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
            image_src="OIP.jfif",  # Ruta de la imagen de fondo
            expand=True,
            alignment=ft.alignment.top_left,
            width=800,
            height=900
        )
    )

    page.update()  # Actualizar la página para reflejar los cambios

def configurar_ventana_juego(page: ft.Page):
    page.clean()  # Limpiar la página actual
    page.title = "Juego - VOLTIUM"
    page.bgcolor = colors.WHITE
    page.window_width = 1024  # Ancho de la ventana del juego
    page.window_height = 768  # Alto de la ventana del juego

    # Aquí puedes agregar los elementos del juego
    game_title = ft.Text("¡Bienvenido al juego!", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú", on_click=volver_al_menu_click, width=150, height=40)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    game_title,
                    ft.Container(
                        content=volver_button,
                        alignment=ft.alignment.top_right
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.alignment.top_left,
            width=1024,
            height=768
        )
    )

    page.update()  # Actualizar la página para reflejar los cambios

ft.app(target=main)