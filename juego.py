import flet as ft
from flet import colors

def configurar_ventana_juego(page: ft.Page, volver_al_menu):
    def volver_al_menu_click(e):
        volver_al_menu(page)

    def modo_facil_click(e):
        configurar_ventana_facil(page, volver_al_menu)

    def modo_medio_click(e):
        configurar_ventana_medio(page, volver_al_menu)

    def modo_dificil_click(e):
        configurar_ventana_dificil(page, volver_al_menu)

    page.clean()  # Limpiar la página actual
    page.title = "Juego - VOLTIUM"
    page.bgcolor = colors.WHITE
    page.window_width = 800  # Ancho de la ventana del juego
    page.window_height = 900  # Alto de la ventana del juego

    # Aquí puedes agregar los elementos del juego
    game_title = ft.Text("¡Bienvenido al juego!", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú", on_click=volver_al_menu_click, width=150, height=40)
    facil_button = ft.ElevatedButton(text="Modo de Juego Fácil", on_click=modo_facil_click, width=200, height=50)
    medio_button = ft.ElevatedButton(text="Modo de Juego Medio", on_click=modo_medio_click, width=200, height=50)
    dificil_button = ft.ElevatedButton(text="Modo de Juego Difícil", on_click=modo_dificil_click, width=200, height=50)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    game_title,
                    facil_button,
                    medio_button,
                    dificil_button,
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

def configurar_ventana_facil(page: ft.Page, volver_al_menu):
    def volver_al_menu_click(e):
        volver_al_menu(page)

    page.clean()
    page.title = "Modo de Juego Fácil"
    page.bgcolor = colors.WHITE
    page.window_width = 800
    page.window_height = 900

    facil_title = ft.Text("Modo de Juego Fácil", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú", on_click=volver_al_menu_click, width=150, height=40)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    facil_title,
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

    page.update()

def configurar_ventana_medio(page: ft.Page, volver_al_menu):
    def volver_al_menu_click(e):
        volver_al_menu(page)

    page.clean()
    page.title = "Modo de Juego Medio"
    page.bgcolor = colors.WHITE
    page.window_width = 800
    page.window_height = 900

    medio_title = ft.Text("Modo de Juego Medio", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú", on_click=volver_al_menu_click, width=150, height=40)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    medio_title,
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

    page.update()

def configurar_ventana_dificil(page: ft.Page, volver_al_menu):
    def volver_al_menu_click(e):
        volver_al_menu(page)

    page.clean()
    page.title = "Modo de Juego Difícil"
    page.bgcolor = colors.WHITE
    page.window_width = 800
    page.window_height = 900

    dificil_title = ft.Text("Modo de Juego Difícil", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú", on_click=volver_al_menu_click, width=150, height=40)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    dificil_title,
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

    page.update()
