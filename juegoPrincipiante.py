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

# Variable global para mantener las fichas disponibles
fichas_disponibles = []

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

def seleccionar_ficha_aleatoria():
    """
    Selecciona una ficha aleatoria de las disponibles y la remueve de la lista
    """
    global fichas_disponibles
    if not fichas_disponibles:
        fichas_disponibles = crear_fichas_domino()
    ficha = random.choice(fichas_disponibles)
    fichas_disponibles.remove(ficha)
    return ficha

def repartir_fichas():
    """
    Reparte las fichas entre jugador, aplicación y pozo
    """
    global fichas_disponibles
    if not fichas_disponibles:
        fichas_disponibles = crear_fichas_domino()
    
    # Repartir 15 fichas para el jugador
    fichas_jugador = []
    for _ in range(15):
        ficha = random.choice(fichas_disponibles)
        fichas_jugador.append(ficha)
        fichas_disponibles.remove(ficha)
    
    # Repartir 15 fichas para la aplicación
    fichas_app = []
    for _ in range(15):
        ficha = random.choice(fichas_disponibles)
        fichas_app.append(ficha)
        fichas_disponibles.remove(ficha)
    
    # Las fichas restantes serán el pozo
    pozo = fichas_disponibles.copy()
    
    return fichas_jugador, fichas_app, pozo

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

def crear_fichas_jugador_row(fichas):
    """Crea una fila de fichas visibles para el jugador"""
    return ft.Row(
        controls=[crear_ficha_visual(f.numero1, f.numero2) for f in fichas],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
    )

def crear_fichas_app_row(cantidad):
    """Crea una fila de fichas ocultas para la aplicación"""
    ficha_oculta = ft.Container(
        width=60,
        height=120,
        bgcolor=colors.BROWN,
        border_radius=5
    )
    return ft.Row(
        controls=[ficha_oculta for _ in range(cantidad)],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
    )

def crear_pozo_column(fichas):
    """Crea una columna de fichas visibles para el pozo"""
    return ft.Column(
        controls=[crear_ficha_visual(f.numero1, f.numero2) for f in fichas],
        scroll=ft.ScrollMode.AUTO,
        spacing=5,
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
    volver_button = ft.ElevatedButton(
        text="Volver al menú",
        on_click=volver_al_menu_principal_click,
        width=200,
        height=50
    )

    # Repartir fichas
    ficha_central = seleccionar_ficha_aleatoria()
    fichas_jugador, fichas_app, pozo = repartir_fichas()
    
    # Crear las vistas de las fichas
    fichas_jugador_view = crear_fichas_jugador_row(fichas_jugador)
    fichas_app_view = crear_fichas_app_row(len(fichas_app))
    pozo_view = crear_pozo_column(pozo)

    # Modificar el contenedor principal
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    # Pozo (izquierda)
                    ft.Container(
                        content=pozo_view,
                        alignment=ft.alignment.center_left,
                        width=150,
                    ),
                    # Área principal de juego
                    ft.Container(
                        content=ft.Column(
                            [
                                titulo,
                                # Fichas de la app (arriba)
                                fichas_app_view,
                                # Ficha central
                                ft.Container(
                                    content=crear_ficha_visual(ficha_central.numero1, ficha_central.numero2),
                                    alignment=ft.alignment.center,
                                    padding=20,
                                ),
                                # Fichas del jugador (abajo)
                                fichas_jugador_view,
                                volver_button,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            expand=True,
        )
    )

    page.update()