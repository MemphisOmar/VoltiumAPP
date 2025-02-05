import flet as ft
from ayuda import mostrar_ayuda
import random
from flet import (
    colors
)

# Diccionario de colores y sus números correspondientes
COLORES_DOMINO = {
    0: (colors.BLACK, "Negro"),
    1: (colors.BROWN, "Marrón"),
    2: (colors.RED, "Rojo"),
    3: (colors.ORANGE, "Naranja"), 
    4: (colors.YELLOW, "Amarillo"),
    5: (colors.GREEN, "Verde"),
    6: (colors.BLUE, "Azul"),
    7: (colors.PURPLE, "Púrpura"),
    8: (colors.GREY, "Gris"),  # Corregido a Gris
    9: (colors.WHITE, "Blanco")  # Corregido a Blanco
}

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

def obtener_representacion_valor(numero):
    """Decide aleatoriamente si mostrar el número o su color correspondiente"""
    if random.random() < 0.5:  # 50% de probabilidad para cada representación
        return ("numero", str(numero))
    else:
        color, _ = COLORES_DOMINO[numero]
        return ("color", color)

def crear_contenido_ficha(valor_representacion):
    """Crea el contenido de la ficha según el tipo de representación"""
    tipo, valor = valor_representacion
    if tipo == "numero":
        return ft.Text(valor, size=24, color=colors.BLACK)
    else:  # tipo == "color"
        return ft.Container(
            width=40,
            height=40,
            bgcolor=valor,
            border_radius=20  # Hace el contenedor circular
        )

def crear_ficha_visual(numero1, numero2, es_central=False):
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(obtener_representacion_valor(numero1)),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(obtener_representacion_valor(numero2)),
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

def crear_ficha_visual_horizontal(numero1, numero2, es_central=False):
    """Crea una ficha visual en orientación horizontal"""
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(obtener_representacion_valor(numero1)),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(obtener_representacion_valor(numero2)),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                )
            ],
            spacing=1,
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar los contenedores
        ),
        bgcolor=colors.BLACK,
        padding=1,
        border_radius=5,
        width=122  # Ancho fijo que corresponde a: 60 (ancho contenedor) * 2 + 1 (spacing) + 1 (padding izq/der)
    )

def crear_ficha_visual_jugador(ficha, on_drag_complete=None):
    """Crea una ficha visual arrastrable para el jugador con botón de rotación"""
    def crear_contenedor_numeros():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=crear_contenido_ficha(obtener_representacion_valor(ficha.numero1)),
                        alignment=ft.alignment.center,
                        bgcolor=colors.WHITE,
                        width=60,
                        height=60,
                        border=ft.border.all(1, colors.BLACK)
                    ),
                    ft.Container(
                        content=crear_contenido_ficha(obtener_representacion_valor(ficha.numero2)),
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

    contenedor_numeros = crear_contenedor_numeros()

    def rotar_ficha(e):
        # Intercambiar los números
        ficha.numero1, ficha.numero2 = ficha.numero2, ficha.numero1
        # Actualizar la visualización
        contenedor_numeros.content.controls[0].content = crear_contenido_ficha(obtener_representacion_valor(ficha.numero1))
        contenedor_numeros.content.controls[1].content = crear_contenido_ficha(obtener_representacion_valor(ficha.numero2))
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
                estado_juego.numero_arriba = ficha.numero1
        else:  # posicion == "abajo"
            numero_a_comparar = estado_juego.numero_abajo
            numero_valido = ficha.numero1 == numero_a_comparar
            if numero_valido:
                estado_juego.numero_abajo = ficha.numero2
        
        if numero_valido:
            estado_juego.fichas_jugadas.append(ficha)
            on_ficha_jugada(ficha, posicion)
            
            # Determinar si es una ficha doble
            es_doble = ficha.numero1 == ficha.numero2
            
            # Crear nueva ficha visual según si es doble o no
            if (es_doble):
                ficha_visual = crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2)
            else:
                ficha_visual = crear_ficha_visual(ficha.numero1, ficha.numero2)
            
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

def crear_ficha_pozo(ficha, on_click):
    """Crea una ficha visual del pozo que se puede hacer clic para agregar a la mano"""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(obtener_representacion_valor(ficha.numero1)),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(obtener_representacion_valor(ficha.numero2)),
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
        border_radius=5,
        on_click=lambda e: on_click(ficha),  # Añadir manejador de clic
    )

def crear_pozo_column(fichas, on_ficha_seleccionada):
    """Crea una columna de fichas visibles para el pozo que se pueden seleccionar"""
    return ft.Column(
        controls=[crear_ficha_pozo(f, on_ficha_seleccionada) for f in fichas],
        scroll=ft.ScrollMode.AUTO,
        spacing=5,
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

    def agregar_ficha_del_pozo(ficha):
        # Remover la ficha del pozo
        pozo.remove(ficha)
        # Agregar la ficha a la mano del jugador
        fichas_jugador.append(ficha)
        # Actualizar las vistas
        fichas_jugador_view.controls.append(crear_ficha_visual_jugador(ficha))
        pozo_view.controls = [crear_ficha_pozo(f, agregar_ficha_del_pozo) for f in pozo]
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
    pozo_view = crear_pozo_column(pozo, agregar_ficha_del_pozo)  # Pasar callback

    # Modificar el contenedor principal
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=pozo_view,
                        alignment=ft.alignment.center_left,
                        width=100,
                        margin=0,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                titulo,
                                ft.Container(
                                    content=fichas_app_view,
                                    padding=2,
                                ),
                                ft.Container(
                                    content=area_juego,
                                    height=400,
                                    border=ft.border.all(1, colors.GREY_400),
                                    border_radius=5,
                                    padding=10,
                                ),
                                ft.Container(
                                    content=fichas_jugador_view,
                                    padding=2,
                                ),
                                ft.Container(
                                    content=volver_button,
                                    alignment=ft.alignment.center,
                                    padding=5,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        expand=True,
                        margin=ft.margin.only(right=20),  # Aumentado de 5 a 20
                        padding=ft.margin.only(left=0),
                    ),
                ],
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
        )
    )

    page.update()