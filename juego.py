# juego.py
import flet as ft
from flet import colors

def configurar_ventana_juego(page: ft.Page, volver_al_menu):
    def volver_al_menu_click(e):
        volver_al_menu(page)

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