import flet as ft
from ayuda import mostrar_ayuda
import random
from flet import (
    colors
)

class FichaDomino:
    def __init__(self, identificador, numero1, numero2):
        self.identificador = identificador
        self.numero1 = numero1
        self.numero2 = numero2

    def __str__(self):
        return f"Ficha {self.identificador}: [{self.numero1}|{self.numero2}]"

def crear_fichas_domino():
    """
    Crea las 55 fichas del dominó cubano (del 0 al 9)
    Retorna una lista ordenada de objetos FichaDomino
    """
    fichas = []
    identificador_ficha = 1
    # Crear todas las combinaciones posibles del 0 al 9
    for i in range(10):  # 0 al 9
        for j in range(i, 10):  # desde i hasta 9
            fichas.append(FichaDomino(identificador_ficha, i, j))
            identificador_ficha += 1
    return fichas

def crear_ficha_visual(numero1, numero2):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(str(numero1), size=24, color=colors.BLACK),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=ft.Text(str(numero2), size=24, color=colors.BLACK),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                )
            ],
            spacing=1,
        ),
        bgcolor=colors.BLACK,
        padding=1,
        border_radius=5
    )

def configurar_ventana_domino(page: ft.Page, volver_al_menu_principal):
    def volver_al_menu_principal_click(e):
        volver_al_menu_principal(page)

    page.clean()
    page.title = "DOMINO - Principiante"
    page.bgcolor = "#b9b3a7"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.margin = 0

    # Título de la página
    titulo = ft.Text("Modo Principiante", size=30, color=colors.BLACK)
    volver_button=ft.ElevatedButton(text="Volver al menú principal", on_click=volver_al_menu_principal_click, width=200, height=50)
    
    # Botón para volver al menú
    volver_button = ft.ElevatedButton(
        text="Volver al menú",
        on_click=volver_al_menu_principal_click,
        width=200,
        height=50
    )

    # Crear la base de fichas ordenada
    base_fichas = crear_fichas_domino()
    
    # Ejemplo de cómo acceder a las fichas:
    # for ficha in base_fichas:
    #     print(ficha)  # Mostrará: Ficha 1: [0|0], Ficha 2: [0|1], etc.

    # Crear grid de fichas
    grid = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=0.5,
        spacing=10,
        run_spacing=10,
    )

    # Agregar fichas visuales al grid
    for ficha in base_fichas:
        grid.controls.append(crear_ficha_visual(ficha.numero1, ficha.numero2))

    # Modificar el contenedor principal para incluir el grid de fichas
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    titulo,
                    ft.Container(
                        content=grid,
                        padding=20,
                        expand=True
                    ),
                    ft.Container(
                        content=volver_button,
                        alignment=ft.alignment.bottom_right
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.alignment.top_center,
            width=1024,
            height=768
        )
    )

    page.update()