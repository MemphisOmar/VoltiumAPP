import flet as ft
from flet import colors

def configurar_ventana_juego(page: ft.Page, volver_al_menu_principal):
    def volver_al_menu_principal_click(e):
        volver_al_menu_principal(page)

    def modo_facil_click(e):
        configurar_ventana_facil(page, configurar_ventana_juego, volver_al_menu_principal)

    def modo_medio_click(e):
        configurar_ventana_medio(page, configurar_ventana_juego, volver_al_menu_principal)

    def modo_dificil_click(e):
        configurar_ventana_dificil(page, configurar_ventana_juego, volver_al_menu_principal)

    page.clean()  # Limpiar la página actual
    page.title = "Juego - VOLTIUM"
    page.bgcolor = "#fff1b9"
    page.window_width = 800  # Ancho de la ventana del juego
    page.window_height = 900  # Alto de la ventana del juego


    game_title = ft.Text("Selecciona el modo de juego", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú principal", on_click=volver_al_menu_principal_click, width=200, height=50)
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

    page.update()  

def configurar_ventana_facil(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    page.clean()
    page.title = "Modo de Juego Fácil"
    page.bgcolor = colors.WHITE
    page.window_width = 800
    page.window_height = 900

    facil_title = ft.Text("Modo de Juego Fácil", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú de modos", on_click=volver_al_menu_click, width=200, height=50)

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

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="resistor_facil.png")
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente el contenido
            ),
            expand=True,
            alignment=ft.alignment.top_center,  # Alinear el contenedor en la parte superior y centrado
            width=1024,
            height=768
        )
    )


    page.update()

def configurar_ventana_medio(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    page.clean()
    page.title = "Modo de Juego Medio"
    page.bgcolor = colors.WHITE
    page.window_width = 800
    page.window_height = 900

    medio_title = ft.Text("Modo de Juego Medio", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú de modos", on_click=volver_al_menu_click, width=200, height=50)

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

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="resistor_medio.png")
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),

            expand=True,
            alignment=ft.alignment.center,
            width=1024,
            height=768
        )
    )

    page.update()

def configurar_ventana_dificil(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    page.clean()
    page.title = "Modo de Juego Difícil"
    page.bgcolor = colors.WHITE
    page.window_width = 800
    page.window_height = 900

    dificil_title = ft.Text("Modo de Juego Difícil", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(text="Volver al menú de modos", on_click=volver_al_menu_click, width=200, height=50)

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

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="resistor_dificil.png")
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),

            expand=True,
            alignment=ft.alignment.center,
            width=1024,
            height=768
        )
    )

    page.update()
