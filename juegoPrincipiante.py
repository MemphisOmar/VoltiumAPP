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

class EstadoJuego:
    def __init__(self, ficha_central):
        self.ficha_central = ficha_central
        self.numero_arriba = ficha_central.numero1  # Cambiado de numero_izquierda
        self.numero_abajo = ficha_central.numero2   # Cambiado de numero_derecha
        self.fichas_jugadas = []
        self.fichas_arriba = []  # Nueva lista para fichas colocadas arriba
        self.fichas_abajo = []   # Nueva lista para fichas colocadas abajo

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

def crear_ficha_visual(numero1, numero2, es_central=False):
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE  # Cambiado a un color más visible
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(str(numero1), size=24, color=colors.BLACK),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=ft.Text(str(numero2), size=24, color=colors.BLACK),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
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

def crear_ficha_visual_jugador(ficha, on_drag_complete=None):
    """Crea una ficha visual arrastrable para el jugador con botón de rotación"""
    contenedor_numeros = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(str(ficha.numero1), size=24, color=colors.BLACK),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=ft.Text(str(ficha.numero2), size=24, color=colors.BLACK),
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

    def rotar_ficha(e):
        # Intercambiar los números
        ficha.numero1, ficha.numero2 = ficha.numero2, ficha.numero1
        # Actualizar la visualización
        numeros = contenedor_numeros.content.controls
        numeros[0].content.value = str(ficha.numero1)
        numeros[1].content.value = str(ficha.numero2)
        e.control.page.update()

    boton_rotar = ft.IconButton(
        icon=ft.icons.ROTATE_RIGHT,
        icon_color=colors.BLACK,
        icon_size=20,
        on_click=rotar_ficha,
        style=ft.ButtonStyle(
            bgcolor=colors.BLUE_GREY_200,
            padding=5,
        ),
        width=30,
        height=30,
    )

    return ft.Draggable(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    boton_rotar,
                    contenedor_numeros
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=5),
        ),
        data=ficha  # Almacenar la ficha original como data
    )

def crear_zona_destino(page: ft.Page, estado_juego, posicion, on_ficha_jugada, area_juego):
    """Crea una zona donde se pueden soltar las fichas"""
    def on_accept(e):
        ficha = page.get_control(e.src_id).data
        
        # Validar coincidencia de números
        if posicion == "arriba":
            numero_a_comparar = estado_juego.numero_arriba
            numero_valido = ficha.numero2 == numero_a_comparar
            if numero_valido:
                estado_juego.numero_arriba = ficha.numero1  # Actualizar con el nuevo número superior
        else:  # posicion == "abajo"
            numero_a_comparar = estado_juego.numero_abajo
            numero_valido = ficha.numero1 == numero_a_comparar
            if numero_valido:
                estado_juego.numero_abajo = ficha.numero2  # Actualizar con el nuevo número inferior
        
        if numero_valido:
            estado_juego.fichas_jugadas.append(ficha)
            on_ficha_jugada(ficha, posicion)
            
            # Crear nueva ficha visual (asegurarse que no sea central)
            ficha_visual = crear_ficha_visual(ficha.numero1, ficha.numero2, es_central=False)
            
            # Determinar índices y actualizar el área de juego
            if posicion == "arriba":
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[0]
                    # Reemplazar la zona actual con la ficha
                    area_juego.controls[indice_actual] = ficha_visual
                    # Crear nueva zona arriba
                    nueva_zona = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego)
                    area_juego.controls.insert(0, nueva_zona)
            else:  # posicion == "abajo"
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[-1]
                    # Reemplazar la zona actual con la ficha
                    area_juego.controls[indice_actual] = ficha_visual
                    # Crear nueva zona abajo
                    nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego)
                    area_juego.controls.append(nueva_zona)
            
            page.update()
            return True
        return False

    return ft.DragTarget(
        content=ft.Container(
            width=70,
            height=140,
            border=ft.border.all(2, colors.GREY_400),
            border_radius=5,
            bgcolor="#E0E0E033",
            content=ft.Column(
                controls=[
                    ft.Container(
                        height=70,
                        width=70,
                        border=ft.border.all(1, colors.GREY_400)  # Removido el estilo DASHED
                    ),
                    ft.Container(
                        height=70,
                        width=70,
                        border=ft.border.all(1, colors.GREY_400)  # Removido el estilo DASHED
                    )
                ],
                spacing=0,
            )
        ),
        on_accept=on_accept
    )

def crear_fichas_jugador_row(fichas, estado_juego, page):
    """Crea una fila de fichas arrastrables para el jugador"""
    return ft.Row(
        controls=[crear_ficha_visual_jugador(f) for f in fichas],
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
    estado_juego = EstadoJuego(ficha_central)
    fichas_jugador, fichas_app, pozo = repartir_fichas()

    def on_ficha_jugada(ficha, lado):
        # Remover la ficha jugada de la mano del jugador
        for control in fichas_jugador_view.controls[:]:
            if control.data.identificador == ficha.identificador:
                fichas_jugador_view.controls.remove(control)
                break
        page.update()

    # Área de juego central scrolleable
    area_juego = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,  # Hacer scrolleable
        height=400,                 # Altura fija para el área de juego
    )

    # Crear las zonas de destino y configurar área de juego inicial
    zona_arriba = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego)
    zona_abajo = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego)
    ficha_central_visual = crear_ficha_visual(ficha_central.numero1, ficha_central.numero2, es_central=True)

    # Inicializar el área de juego con la ficha central y las zonas
    area_juego.controls = [
        zona_arriba,
        ficha_central_visual,
        zona_abajo
    ]

    # Crear las vistas
    fichas_jugador_view = crear_fichas_jugador_row(fichas_jugador, estado_juego, page)
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
                                fichas_app_view,
                                # Envolver area_juego en un contenedor con altura fija
                                ft.Container(
                                    content=area_juego,
                                    height=400,
                                    border=ft.border.all(1, colors.GREY_400),
                                    border_radius=5,
                                    padding=10,
                                ),
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