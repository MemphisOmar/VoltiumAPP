import flet as ft
from ayuda import mostrar_ayuda
import random
import time
import threading
import os
import json
from db_manager import DBManager
from sesion_manager import SesionManager
from flet import (
    colors
)


class Timer:
    def __init__(self):
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.total_time += time.time() - self.start_time
            self.is_running = False

    def reset(self):
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def get_current_time(self):
        if not self.is_running:
            return self.total_time
        return self.total_time + (time.time() - self.start_time)

    def get_time_string(self):
        current_time = self.get_current_time()
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

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
    8: (colors.GREY, "Gris"),  
    9: (colors.WHITE, "Blanco")  
}

class FichaDomino:
    def __init__(self, identificador, numero1, numero2):
        self.identificador = identificador
        self.numero1 = numero1
        self.numero2 = numero2
        # Agregar representaciones iniciales para cada número
        self.repr1 = obtener_representacion_valor(numero1)
        self.repr2 = obtener_representacion_valor(numero2)

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
    # Reiniciar las fichas disponibles al comenzar un nuevo juego
    fichas_disponibles = crear_fichas_domino()
    
    # Crear una copia de las fichas disponibles para manipular
    fichas_temp = fichas_disponibles.copy()
    
    # Repartir 7 fichas para el jugador
    fichas_jugador = []
    for _ in range(7):
        ficha = random.choice(fichas_temp)
        fichas_jugador.append(ficha)
        fichas_temp.remove(ficha)
    
    # Repartir 7 fichas para la aplicación
    fichas_app = []
    for _ in range(7):
        ficha = random.choice(fichas_temp)
        fichas_app.append(ficha)
        fichas_temp.remove(ficha)
    
    # Las fichas restantes serán el pozo
    pozo = fichas_temp.copy()
    
    # Actualizar las fichas disponibles globales
    fichas_disponibles = pozo.copy()
    
    return fichas_jugador, fichas_app, pozo

def obtener_representacion_valor(numero):
    """Decide aleatoriamente si mostrar el número o su color correspondiente"""
    if random.random() < 0.5:  # 50% de probabilidad para cada representación
        return ("numero", str(numero))
    else:
        color, _ = COLORES_DOMINO[numero]
        return ("color", color)

def crear_representacion_puntos(numero):
    """Crea una representación visual de un número como puntos de dominó tradicional"""
    # Definir posiciones para los puntos según el número (0-9)
    # Las posiciones están en una cuadrícula 3x3 escalada a un contenedor de 40x40
    posiciones = {
        0: [],  # Sin puntos
        1: [(20, 20)],  # Centro
        2: [(10, 10), (30, 30)],  # Esquinas opuestas
        3: [(10, 10), (20, 20), (30, 30)],  # Diagonal con centro
        4: [(10, 10), (10, 30), (30, 10), (30, 30)],  # Esquinas
        5: [(10, 10), (10, 30), (20, 20), (30, 10), (30, 30)],  # Esquinas y centro
        6: [(10, 10), (10, 20), (10, 30), (30, 10), (30, 20), (30, 30)],  # Lados izquierdo y derecho
        7: [(10, 10), (10, 20), (10, 30), (20, 20), (30, 10), (30, 20), (30, 30)],  # Lados y centro
        8: [(10, 10), (10, 20), (10, 30), (20, 10), (20, 30), (30, 10), (30, 20), (30, 30)],  # Lados y aristas sin centro
        9: [(10, 10), (10, 20), (10, 30), (20, 10), (20, 20), (20, 30), (30, 10), (30, 20), (30, 30)]  # Cuadrícula completa
    }
    
    # Crear un stack con los puntos en las posiciones correspondientes
    stack = ft.Stack(
        controls=[
            ft.Container(
                width=8,
                height=8,
                border_radius=4,
                bgcolor=colors.BLACK,
                left=x - 4,
                top=y - 4
            )
            for x, y in posiciones.get(numero, [])
        ],
        width=40,
        height=40
    )
    
    return stack

def crear_contenido_ficha(valor_representacion):
    """Crea el contenido de la ficha según el tipo de representación"""
    tipo, valor = valor_representacion
    if (tipo == "numero"):
        return crear_representacion_puntos(int(valor))
    else:  # tipo == "color"
        return ft.Container(
            width=60,  # Ancho completo de la mitad de la ficha
            height=60,  # Alto completo de la mitad de la ficha
            bgcolor=valor,
            border=ft.border.all(0.5, colors.BLACK)
        )

# Añadir un parámetro para el color del borde
def crear_ficha_visual(numero1, numero2, es_central=False, repr1=None, repr2=None, es_computadora=False):
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    color_borde = colors.BROWN if es_computadora else colors.BLACK
    
    repr1 = repr1 or obtener_representacion_valor(numero1)
    repr2 = repr2 or obtener_representacion_valor(numero2)
    
    tipo1, _ = repr1
    tipo2, _ = repr2
    
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(repr1),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo if tipo1 == "numero" else None,
                    width=40,
                    height=40,
                    border=ft.border.all(1, color_borde) if tipo1 == "numero" else None
                ),
                ft.Container(
                    content=crear_contenido_ficha(repr2),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo if tipo2 == "numero" else None,
                    width=40,
                    height=40,
                    border=ft.border.all(1, color_borde) if tipo2 == "numero" else None
                )
            ],
            spacing=1,
        ),
        bgcolor=color_borde,
        padding=1,
        border_radius=5
    )

# Añadir el mismo parámetro para la versión horizontal
def crear_ficha_visual_horizontal(numero1, numero2, es_central=False, repr1=None, repr2=None, es_computadora=False):
    """Crea una ficha visual en orientación horizontal"""
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    color_borde = colors.BROWN if es_computadora else colors.BLACK
    
    repr1 = repr1 or obtener_representacion_valor(numero1)
    repr2 = repr2 or obtener_representacion_valor(numero2)
    
    tipo1, _ = repr1
    tipo2, _ = repr2
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(repr1),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo if tipo1 == "numero" else None,
                    width=40,
                    height=40,
                    border=ft.border.all(1, color_borde) if tipo1 == "numero" else None
                ),
                ft.Container(
                    content=crear_contenido_ficha(repr2),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo if tipo2 == "numero" else None,
                    width=40,
                    height=40,
                    border=ft.border.all(1, color_borde) if tipo2 == "numero" else None
                )
            ],
            spacing=1,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=color_borde,
        padding=1,
        border_radius=5,
        width=82
    )

def crear_ficha_visual_jugador(ficha, on_drag_complete=None):
    """Crea una ficha visual arrastrable para el jugador con botón de rotación"""
    def crear_contenedor_numeros():
        tipo1, _ = ficha.repr1
        tipo2, _ = ficha.repr2
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=crear_contenido_ficha(ficha.repr1),
                        alignment=ft.alignment.center,
                        bgcolor=colors.WHITE if tipo1 == "numero" else None,
                        width=40,
                        height=40,
                        border=ft.border.all(1, colors.BLACK) if tipo1 == "numero" else None
                    ),
                    ft.Container(
                        content=crear_contenido_ficha(ficha.repr2),
                        alignment=ft.alignment.center,
                        bgcolor=colors.WHITE if tipo2 == "numero" else None,
                        width=40,
                        height=40,
                        border=ft.border.all(1, colors.BLACK) if tipo2 == "numero" else None
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
        ficha.numero1, ficha.numero2 = ficha.numero2, ficha.numero1
        ficha.repr1, ficha.repr2 = ficha.repr2, ficha.repr1
        contenedor_numeros.content.controls[0].content = crear_contenido_ficha(ficha.repr1)
        contenedor_numeros.content.controls[1].content = crear_contenido_ficha(ficha.repr2)
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
        data=ficha
    )

def crear_zona_destino(page: ft.Page, estado_juego, posicion, on_ficha_jugada, area_juego, obtener_representacion_forzada=None):
    """Crea una zona donde se pueden soltar las fichas"""
    def on_accept(e):
        ficha = page.get_control(e.src_id).data
        
        if posicion == "arriba":
            numero_a_comparar = estado_juego.numero_arriba
            numero_valido = ficha.numero2 == numero_a_comparar
            if numero_valido:
                estado_juego.numero_arriba = ficha.numero1
        else:
            numero_a_comparar = estado_juego.numero_abajo
            numero_valido = ficha.numero1 == numero_a_comparar
            if numero_valido:
                estado_juego.numero_abajo = ficha.numero2
        
        if numero_valido:
            estado_juego.fichas_jugadas.append(ficha)
            on_ficha_jugada(ficha, posicion)
            
            es_doble = ficha.numero1 == ficha.numero2
            
            if obtener_representacion_forzada:
                repr1_central = obtener_representacion_forzada(ficha.numero1, False)
                repr2_central = obtener_representacion_forzada(ficha.numero2, False)
            else:
                repr1_central = ficha.repr1
                repr2_central = ficha.repr2
            
            ficha_visual = (
                crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2, repr1=repr1_central, repr2=repr2_central)
                if es_doble
                else crear_ficha_visual(ficha.numero1, ficha.numero2, repr1=repr1_central, repr2=repr2_central)
            )
            
            if posicion == "arriba":
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[0]
                    area_juego.controls[indice_actual] = ficha_visual
                    nueva_zona = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                    area_juego.controls.insert(0, nueva_zona)
                    # Mantener centradas las fichas después de agregar una nueva
                    area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            else:
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[-1]
                    area_juego.controls[indice_actual] = ficha_visual
                    nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                    area_juego.controls.append(nueva_zona)
                    # Mantener centradas las fichas después de agregar una nueva
                    area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
            page.update()
            return True
        return False

    return ft.DragTarget(
        content=ft.Container(
            width=50,
            height=100,
            border=ft.border.all(2, colors.GREY_400),
            border_radius=5,
            bgcolor="#E0E0E033",
            content=ft.Column(
                controls=[
                    ft.Container(
                        height=50,
                        width=50,
                        border=ft.border.all(1, colors.GREY_400)
                    ),
                    ft.Container(
                        height=50,
                        width=50,
                        border=ft.border.all(1, colors.GREY_400)
                    )
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
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
                    content=crear_contenido_ficha(ficha.repr1),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=40,
                    height=40,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(ficha.repr2),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=40,
                    height=40,
                    border=ft.border.all(1, colors.BLACK)
                )
            ],
            spacing=1,
        ),
        bgcolor=colors.BLACK,
        padding=1,
        border_radius=5,
        on_click=lambda e: on_click(ficha),
    )

def crear_pozo_column(fichas, on_ficha_seleccionada, fichas_jugador=None, fichas_app=None, ficha_central_presente=True):
    """
    Crea una columna de fichas ocultas para el pozo
    
    Args:
        fichas: Lista de fichas en el pozo
        on_ficha_seleccionada: Función callback cuando se selecciona una ficha
        fichas_jugador, fichas_app, ficha_central_presente: Parámetros no utilizados
    """
    texto_pozo = ft.Text(f"Pozo ({len(fichas)})", size=16, color=colors.BLACK, text_align=ft.TextAlign.CENTER)
    columna_fichas = None

    def actualizar_vista_pozo():
        """Actualiza el contador y las fichas visuales del pozo"""
        texto_pozo.value = f"Pozo ({len(fichas)})"
        columna_fichas.controls = [
            ft.Container(
                width=56,
                height=98,
                bgcolor=colors.WHITE,
                border=ft.border.all(2, "#1B4D3E"),
                border_radius=5,
                margin=ft.margin.only(bottom=5),
                on_click=lambda e, f=ficha: on_ficha_click(e, f)
            ) 
            for ficha in fichas
        ]

    def on_ficha_click(e, ficha):
        if ficha in fichas:
            on_ficha_seleccionada(ficha)
            actualizar_vista_pozo()
            e.control.page.update()

    columna_fichas = ft.Column(
        controls=[
            ft.Container(
                width=56,
                height=98,
                bgcolor=colors.WHITE,
                border=ft.border.all(2, "#1B4D3E"),
                border_radius=5,
                margin=ft.margin.only(bottom=5),
                on_click=lambda e, f=ficha: on_ficha_click(e, f)
            ) 
            for ficha in fichas
        ],
        spacing=2,
        scroll=ft.ScrollMode.AUTO,
        height=800
    )
    
    contenedor_columna = ft.Container(
        content=columna_fichas,
        width=84,
        height=600,
        border=ft.border.all(1, colors.GREY_400),
        border_radius=5,
        padding=7,
        bgcolor="#1B4D3E"
    )
    
    contenedor_columna.actualizar = actualizar_vista_pozo
    
    return ft.Column(
        controls=[
            texto_pozo,
            contenedor_columna
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

def crear_fichas_app_row(cantidad):
    """Crea una fila de fichas ocultas para la aplicación"""
    ficha_oculta = ft.Container(
        width=42,
        height=84,
        bgcolor=colors.WHITE,
        border=ft.border.all(2, "#1B4D3E"),
        border_radius=5
    )
    return ft.Row(
        controls=[ficha_oculta for _ in range(cantidad)],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
    )

def encontrar_ficha_inicial(fichas_jugador, fichas_app):
    """
    Determina quién tiene la ficha más alta y cuál es esa ficha.
    Prioriza dobles y luego suma de números.
    Retorna: (ficha, "jugador"/"app")
    """
    def valor_ficha(ficha):
        if ficha.numero1 == ficha.numero2:
            return (1, ficha.numero1, ficha.numero2)
        return (0, max(ficha.numero1, ficha.numero2), min(ficha.numero1, ficha.numero2))
    
    mejor_ficha_jugador = max(fichas_jugador, key=valor_ficha)
    mejor_ficha_app = max(fichas_app, key=valor_ficha)
    
    if valor_ficha(mejor_ficha_jugador) > valor_ficha(mejor_ficha_app):
        return mejor_ficha_jugador, "jugador"
    return mejor_ficha_app, "app"

class JuegoPrincipiante:
    def __init__(self, page, main_menu):
        self.estado_partida = "DESERTO"  # Estado inicial de la partida
        self.page = page
        self.main_menu = main_menu
        self.timer_active = True
        self.fichas_disponibles = crear_fichas_domino()
        self.game_timer = Timer()
        self.timer_text = ft.Text("00:00", color=colors.WHITE, size=20, weight=ft.FontWeight.BOLD)
        self.modo_central_numeros = random.choice([True, False])
        self.modo_mensaje = ("El tablero central mostrará números y tus fichas colores" 
                            if self.modo_central_numeros else 
                            "El tablero central mostrará colores y tus fichas números")
        self.escala_actual = 1.0
        self.turno_jugador = True
        self.fichas_jugador, self.fichas_app, self.pozo = repartir_fichas()
        self.fichas_jugador = self.convertir_fichas_segun_modo(self.fichas_jugador, True)
        self.fichas_app = self.convertir_fichas_segun_modo(self.fichas_app, False)
        self.ficha_central, self.quien_empieza = encontrar_ficha_inicial(self.fichas_jugador, self.fichas_app)
        
        # Eliminar la ficha inicial de las fichas del jugador si el jugador empieza
        if self.quien_empieza == "jugador":
            self.fichas_jugador = [f for f in self.fichas_jugador if f.identificador != self.ficha_central.identificador]
        elif self.quien_empieza == "app":
            self.fichas_app = [f for f in self.fichas_app if f.identificador != self.ficha_central.identificador]

        self.turno_jugador = self.quien_empieza != "jugador"
        self.estado_juego = EstadoJuego(self.ficha_central)
        
        # Para el diálogo de "Ver Tablero Completo" - almacenar datos en lugar de controles visuales
        self.datos_fichas_arriba = []  # Lista de diccionarios con datos de fichas
        self.datos_fichas_abajo = []   # Lista de diccionarios con datos de fichas

        self.page.clean()
        self.page.title = "DOMINO - Principiante"
        self.page.bgcolor = "#1B4D3E"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window_width = 720
        self.page.window_height = 1280
        self.page.window_resizable = False
        self.page.padding = 0
        self.page.margin = 0
        self.titulo = ft.Text("Modo Principiante", size=24, color=colors.BLACK)
        self.volver_button = ft.ElevatedButton(
            text="FINALIZAR JUEGO",
            on_click=self.finalizar_juego,
            width=120,
            height=40
        )
        self.boton_ver_juego_completo = ft.ElevatedButton(
            text="Ver Tablero",
            on_click=self.mostrar_juego_completo_dialogo,  # Cambiar de vuelta al método original
            width=120,
            height=40
        )
        self.ficha_central.repr1 = self.obtener_representacion_forzada(self.ficha_central.numero1, False)
        self.ficha_central.repr2 = self.obtener_representacion_forzada(self.ficha_central.numero2, False)
        self.dlg = ft.AlertDialog(
            title=ft.Text(
                "Modo de Juego",
                size=18,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                self.modo_mensaje,
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            padding=ft.padding.all(5)
                        ),
                        ft.Divider(height=1, color=colors.BLUE_GREY_200),
                        ft.Container(
                            content=ft.Text(
                                self.get_mensaje_ficha_inicial(self.quien_empieza, self.ficha_central, self.modo_central_numeros),
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            padding=ft.padding.all(5)
                        )
                    ],
                    tight=True,
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(5),
                width=280
            ),
            actions=[
                ft.ElevatedButton(
                    "Entendido",
                    on_click=self.cerrar_dialogo,
                    style=ft.ButtonStyle(
                        color=colors.WHITE,
                        bgcolor=colors.BLUE_400
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.area_juego = ft.Column(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,  # Alineación vertical al centro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alineación horizontal al centro
            spacing=5,
            # Cambiamos NONE (que no existe) por AUTO y establecemos el valor a False directamente
            scroll=False,  # Deshabilitamos el scroll en esta columna
            height=400,
        )
        self.zona_arriba = self.crear_zona_destino("arriba")
        self.zona_abajo = self.crear_zona_destino("abajo")
        self.es_ficha_central_doble = self.ficha_central.numero1 == self.ficha_central.numero2
        self.ficha_central_visual = (
            crear_ficha_visual_horizontal(self.ficha_central.numero1, self.ficha_central.numero2, es_central=True, repr1=self.ficha_central.repr1, repr2=self.ficha_central.repr2)
            if self.es_ficha_central_doble
            else crear_ficha_visual(self.ficha_central.numero1, self.ficha_central.numero2, es_central=True, repr1=self.ficha_central.repr1, repr2=self.ficha_central.repr2)
        )
        # Guardar datos de la ficha central para el diálogo
        self.datos_ficha_central = {
            "numero1": self.ficha_central.numero1,
            "numero2": self.ficha_central.numero2,
            "repr1": self.ficha_central.repr1,
            "repr2": self.ficha_central.repr2,
            "es_doble": self.es_ficha_central_doble,
            "es_computadora": False,
            "es_central": True
        }
        self.area_juego.controls = [
            self.zona_arriba,
            self.ficha_central_visual,
            self.zona_abajo
        ]
        
        # Contenedor interno escalable con tamaño adaptable
        self.area_juego_escalable = ft.Container(
            content=self.area_juego,
            scale=self.escala_actual,
            alignment=ft.alignment.center,  # Centrar el contenido
            expand=True,
        )
        
        # Contenedor fijo con capacidad de scroll
        self.contenedor_area_juego_fijo = ft.Container(
            content=ft.Column(
                [self.area_juego_escalable],
                scroll=ft.ScrollMode.AUTO,  # Mantenemos el scroll aquí
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=360,  # Reducido de 400 a 360
            width=500,
            border=ft.border.all(1, colors.GREY_400),
            border_radius=5,
            padding=5,
            bgcolor="#1B4D3E",
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            alignment=ft.alignment.center,  # Centrar todo el contenido dentro del contenedor
        )
        
        self.texto_zoom = ft.Text("100%", size=14, weight=ft.FontWeight.BOLD)
        self.controles_zoom = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.ZOOM_OUT,
                    icon_color=colors.WHITE,
                    on_click=self.disminuir_zoom,
                    tooltip="Alejar"
                ),
                self.texto_zoom,
                ft.IconButton(
                    icon=ft.icons.ZOOM_IN,
                    icon_color=colors.WHITE,
                    on_click=self.aumentar_zoom,
                    tooltip="Acercar"
                ),
                ft.IconButton(
                    icon=ft.icons.REFRESH,
                    icon_color=colors.WHITE,
                    on_click=self.restablecer_zoom,
                    tooltip="Restablecer zoom"
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )
        
        self.fichas_jugador_view = crear_fichas_jugador_row(self.fichas_jugador, self.estado_juego, self.page)
        self.fichas_app_view = crear_fichas_app_row(len(self.fichas_app))
        self.pozo_view = crear_pozo_column(self.pozo, self.agregar_ficha_del_pozo)
        self.boton_jugar_oponente = ft.ElevatedButton(
            text="Pasar Turno",
            tooltip="Hacer jugar al oponente",
            on_click=self.jugador_pasa_turno,  # Changed to new method
            width=120,
            height=40,
            style=ft.ButtonStyle(
                color=colors.WHITE,
                bgcolor=colors.BLUE_700
            )
        )
        self.texto_turno = ft.Text("Tu turno" if self.quien_empieza != "jugador" else "Turno PC", 
                                color=colors.WHITE, weight=ft.FontWeight.BOLD, size=16)
        self.indicador_turno = ft.Container(
            content=self.texto_turno,
            width=100,
            height=35,  # Reducido de 40 a 35
            bgcolor=colors.GREEN if self.quien_empieza != "jugador" else colors.RED,
            border_radius=5,
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=5)  # Reducido de 10 a 5
        )
        self.timer_container = ft.Container(
            content=self.timer_text,
            bgcolor=colors.BLUE_GREY_900,
            padding=10,
            border_radius=5,
            margin=ft.margin.only(bottom=10)
        )
        self.page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    self.pozo_view,
                                    self.timer_container,
                                    self.boton_ver_juego_completo, # Botón añadido aquí
                                    self.volver_button
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            alignment=ft.alignment.center_left,
                            width=140,
                            margin=0,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    self.titulo,
                                    ft.Container(
                                        content=self.fichas_app_view,
                                        padding=2,
                                        height=90,  # Reducido de 100 a 90
                                    ),
                                    ft.Container(
                                        content=self.boton_jugar_oponente,
                                        alignment=ft.alignment.center,
                                        padding=3,  # Reducido de 5 a 3
                                    ),
                                    self.contenedor_area_juego_fijo,  # Este contenedor se modificará abajo
                                    ft.Row(
                                        [self.indicador_turno, self.controles_zoom],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        spacing=5,
                                    ),  # Unir elementos para ahorrar espacio
                                    ft.Container(
                                        content=self.fichas_jugador_view,
                                        padding=2,
                                        height=180,  # Ajustado de 200 a 180 para compactar
                                        margin=ft.margin.only(top=10),  # Añadir margen superior
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=3,  # Reducido de 5 a 3
                            ),
                            expand=True,
                            margin=ft.margin.only(right=10),
                            padding=0,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                margin=ft.margin.only(bottom=20),  # Añadir margen inferior para empujar todo hacia arriba
            )
        )
        if not self.turno_jugador:
            threading.Timer(2.0, self.colocar_ficha_especial).start()
        self.actualizar_zoom_automatico()
        self.page.update()
        self.iniciar_temporizador()
        
        # Obtener user_id desde user_profile.json
        profile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_profile.json")
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                user_profile = json.load(f)
                self.user_id = user_profile.get("id")
        else:
            self.user_id = None
            print("No se encontró el perfil de usuario.")

        if self.user_id:
            self.sesion_manager = SesionManager(self.user_id)
            self.sesion_manager.incrementar_partidas()  # Incrementa partidas al iniciar el juego
            # Obtener el número de partida actual para este usuario
            self.numero_partida = self.sesion_manager.obtener_datos()["partidas"]
        else:
            self.sesion_manager = None
            self.numero_partida = 1
        self.tiempo_partida = 0  # Para almacenar el tiempo jugado en la partida

    def cleanup(self):
        self.timer_active = False
        if hasattr(self, 'timer_thread'):
            self.timer_thread.join()

    def update_timer(self):
        while self.timer_active and hasattr(self, 'tiempo_restante'):
            try:
                if self.page.app_running:
                    self.tiempo_restante -= 1
                    self.text_tiempo.value = f"Tiempo: {self.tiempo_restante}"
                    self.page.update()
                time.sleep(1)
            except Exception as e:
                print(f"Error en temporizador: {e}")
                break
        return False

    def finalizar_juego(self, e):
        self.cleanup()
        if self.game_timer:
            self.game_timer.stop()
            segundos_jugados = int(self.game_timer.get_current_time())
            # Guardar el tiempo en la base de datos de sesiones
            if self.sesion_manager and segundos_jugados > 0:
                self.sesion_manager.incrementar_tiempo(segundos_jugados)
            # Guardar la partida individual
            h = segundos_jugados // 3600
            m = (segundos_jugados % 3600) // 60
            s = segundos_jugados % 60
            tiempo_str = f"{h:02d}:{m:02d}:{s:02d}"
            if self.sesion_manager:
                self.sesion_manager.registrar_partida_individual(self.numero_partida, tiempo_str, self.estado_partida)
        if self.main_menu:
            self.main_menu(self.page)
        
    def actualizar_tiempo(self):
        if hasattr(self, 'game_timer') and hasattr(self, 'timer_text'):
            while self.timer_active:
                try:
                    if self.page.app_running:
                        self.timer_text.value = self.game_timer.get_time_string()
                        self.page.update()
                    time.sleep(1)
                except Exception as e:
                    print(f"Error actualizando temporizador: {e}")
                    break

    def iniciar_temporizador(self):
        self.game_timer.start()
        self.timer_thread = threading.Thread(target=self.actualizar_tiempo)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def cerrar_dialogo(self, e):
        self.dlg.open = False
        self.page.update()

    def calcular_zoom_automatico(self):
        num_fichas = len([c for c in self.area_juego.controls if not isinstance(c, ft.DragTarget)])
        
        if num_fichas <= 3:
            return 0.95
        elif num_fichas <= 6:
            return 0.7
        elif num_fichas <= 9:
            return 0.55
        elif num_fichas <= 12:
            return 0.40
        else:
            return 0.25

    def actualizar_zoom_automatico(self):
        nuevo_zoom = self.calcular_zoom_automatico()
        # Actualizar el zoom del contenido
        self.area_juego_escalable.scale = nuevo_zoom
        self.texto_zoom.value = f"{int(nuevo_zoom * 100)}%"
        
        # Ajustar el tamaño del área de juego según el zoom
        self.ajustar_tamano_area_juego(nuevo_zoom)
        self.page.update()

    def aumentar_zoom(self, e):
        if self.escala_actual < 2.0:
            self.escala_actual += 0.1
            self.actualizar_zoom()
            
    def disminuir_zoom(self, e):
        if self.escala_actual > 0.1:
            self.escala_actual -= 0.1
            self.actualizar_zoom()
            
    def restablecer_zoom(self, e):
        self.escala_actual = 1.0
        self.actualizar_zoom()
        
    def actualizar_zoom(self):
        # Actualizar el zoom del área de juego escalable
        self.area_juego_escalable.scale = self.escala_actual
        self.texto_zoom.value = f"{int(self.escala_actual * 100)}%"
        
        # Ajustar el tamaño del área de juego según el zoom
        self.ajustar_tamano_area_juego(self.escala_actual)
        self.page.update()
    
    def ajustar_tamano_area_juego(self, zoom_level):
        """
        Ajusta el tamaño del área de juego basado en el nivel de zoom
        para asegurar que todo el contenido sea visible.
        """
        # Calcular un factor de expansión inverso al zoom
        # Cuando zoom es más pequeño (alejar), el área debe expandirse más
        num_fichas = len([c for c in self.area_juego.controls if not isinstance(c, ft.DragTarget)])
        
        # Calcular ancho base según el número de fichas horizontales
        base_width = max(500, num_fichas * 50)  # Ancho mínimo de 500px
        
        # El ancho y alto se ajustan inversamente al zoom para mostrar más contenido cuando se aleja
        if zoom_level < 1.0:
            # Ajustar dimensiones para mostrar más contenido a menor zoom
            self.area_juego.width = base_width / zoom_level
            
            # Si hay muchas fichas, permitir que sea más alto
            if num_fichas > 10:
                self.area_juego.height = 600 / zoom_level
            else:
                self.area_juego.height = 400 / zoom_level
        else:
            # En zoom normal o aumentado, mantener dimensiones estándar
            self.area_juego.width = base_width
            self.area_juego.height = 400
    
    def on_ficha_jugada(self, ficha, lado):
        self.turno_jugador = False
        ficha.repr1 = self.obtener_representacion_forzada(ficha.numero1, False)
        ficha.repr2 = self.obtener_representacion_forzada(ficha.numero2, False)
        
        for control in self.fichas_jugador_view.controls[:]:
            if control.data.identificador == ficha.identificador:
                self.fichas_jugador_view.controls.remove(control)
                break
        
        es_doble = ficha.numero1 == ficha.numero2
        
        # Crear ficha visual para el tablero principal
        ficha_visual = (
            crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2, 
                                          repr1=ficha.repr1, repr2=ficha.repr2)
            if es_doble
            else crear_ficha_visual(ficha.numero1, ficha.numero2, 
                                    repr1=ficha.repr1, repr2=ficha.repr2)
        )
        
        # Guardar datos para el diálogo (no el control visual)
        datos_ficha = {
            "numero1": ficha.numero1,
            "numero2": ficha.numero2,
            "repr1": ficha.repr1,
            "repr2": ficha.repr2,
            "es_doble": es_doble,
            "es_computadora": False,
            "es_central": False
        }
        
        if lado == "arriba":
            self.datos_fichas_arriba.insert(0, datos_ficha)  # Guardar datos para diálogo
            indices_zonas = [i for i, control in enumerate(self.area_juego.controls) 
                             if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[0]
                self.area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = self.crear_zona_destino("arriba")
                self.area_juego.controls.insert(0, nueva_zona)
                self.area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        else:
            self.datos_fichas_abajo.append(datos_ficha)  # Guardar datos para diálogo
            indices_zonas = [i for i, control in enumerate(self.area_juego.controls) 
                             if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[-1]
                self.area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = self.crear_zona_destino("abajo")
                self.area_juego.controls.append(nueva_zona)
                self.area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.actualizar_vista_extremos()
        self.actualizar_zoom_automatico()
        
        if len(self.fichas_jugador_view.controls) == 0:
            mensaje = "¡Has ganado!"
            self.mostrar_mensaje(mensaje)
            return
        
        self.turno_jugador = False
        self.actualizar_indicador_turno()
        self.page.update()

        if not self.turno_jugador:
            threading.Timer(2.0, self.colocar_ficha_especial).start()
        
        self.page.update()

    def finalizar_partida(self):
        # Llamar esto cuando termine una partida
        if self.game_timer:
            self.tiempo_partida = int(self.game_timer.get_current_time())
        else:
            self.tiempo_partida = 0
        if self.sesion_manager and self.tiempo_partida > 0:
            self.sesion_manager.incrementar_tiempo(self.tiempo_partida)

    def marcar_ganador(self):
        self.estado_partida = "GANO"

    def marcar_perdedor(self):
        self.estado_partida = "PERDIO"

    def agregar_ficha_del_pozo(self, ficha):
        if ficha in self.pozo:
            self.pozo.remove(ficha)
            ficha.repr1 = self.obtener_representacion_forzada(ficha.numero1, True)
            ficha.repr2 = self.obtener_representacion_forzada(ficha.numero2, True)
            self.fichas_jugador.append(ficha)
            self.fichas_jugador_view.controls.append(crear_ficha_visual_jugador(ficha))
            mensaje = f"Quedan {len(self.pozo)} fichas en el pozo"
            self.mostrar_mensaje(mensaje)
            self.page.update()

    def actualizar_vista_extremos(self):
        """Actualiza la vista para mostrar solo los extremos del juego"""
        controles = self.area_juego.controls
        if len(controles) <= 5:  # Si hay 5 o menos elementos, mostrar todo
            return
        
        # Obtener los elementos importantes
        zona_arriba = next((c for c in controles if isinstance(c, ft.DragTarget) and c == controles[0]), None)
        primera_ficha = next((c for c in controles[1:2] if not isinstance(c, ft.DragTarget)), None)
        ficha_central = self.ficha_central_visual
        ultima_ficha = next((c for c in controles[-2:-1] if not isinstance(c, ft.DragTarget)), None)
        zona_abajo = next((c for c in controles if isinstance(c, ft.DragTarget) and c == controles[-1]), None)
        
        # Crear indicador de fichas ocultas
        indicador_fichas = ft.Container(
            content=ft.Text("...", size=20, color=colors.GREY_400),
            alignment=ft.alignment.center,
            height=40
        )
        
        # Actualizar controles para mostrar solo los extremos
        nuevos_controles = []
        if zona_arriba:
            nuevos_controles.append(zona_arriba)
        if primera_ficha:
            nuevos_controles.append(primera_ficha)
        nuevos_controles.append(indicador_fichas)
        if ultima_ficha:
            nuevos_controles.append(ultima_ficha)
        if zona_abajo:
            nuevos_controles.append(zona_abajo)
        
        self.area_juego.controls = nuevos_controles

    def mostrar_mensaje(self, mensaje):
        if "ganado" in mensaje:
            self.game_timer.stop()
        dlg = ft.AlertDialog(
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.cerrar_mensaje(e, dlg))
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def cerrar_mensaje(self, e, dlg):
        dlg.open = False
        e.page.update()
    
    def mostrar_juego_completo_dialogo(self, e):
        """Crea y muestra un overlay con todas las fichas jugadas como alternativa al diálogo"""
        print("=== DEBUG: Usando overlay en lugar de diálogo ===")
        
        try:
            # Crear controles igual que antes
            controles_tablero = []
            
            # Añadir fichas de arriba
            for datos_ficha in reversed(self.datos_fichas_arriba):
                if datos_ficha["es_doble"]:
                    ficha_control = crear_ficha_visual_horizontal(
                        datos_ficha["numero1"], datos_ficha["numero2"],
                        repr1=datos_ficha["repr1"], repr2=datos_ficha["repr2"],
                        es_computadora=datos_ficha["es_computadora"],
                        es_central=datos_ficha["es_central"]
                    )
                else:
                    ficha_control = crear_ficha_visual(
                        datos_ficha["numero1"], datos_ficha["numero2"],
                        repr1=datos_ficha["repr1"], repr2=datos_ficha["repr2"],
                        es_computadora=datos_ficha["es_computadora"],
                        es_central=datos_ficha["es_central"]
                    )
                controles_tablero.append(ficha_control)
            
            # Añadir ficha central
            if self.datos_ficha_central["es_doble"]:
                ficha_central_control = crear_ficha_visual_horizontal(
                    self.datos_ficha_central["numero1"], self.datos_ficha_central["numero2"],
                    repr1=self.datos_ficha_central["repr1"], repr2=self.datos_ficha_central["repr2"],
                    es_computadora=self.datos_ficha_central["es_computadora"],
                    es_central=self.datos_ficha_central["es_central"]
                )
            else:
                ficha_central_control = crear_ficha_visual(
                    self.datos_ficha_central["numero1"], self.datos_ficha_central["numero2"],
                    repr1=self.datos_ficha_central["repr1"], repr2=self.datos_ficha_central["repr2"],
                    es_computadora=self.datos_ficha_central["es_computadora"],
                    es_central=self.datos_ficha_central["es_central"]
                )
            controles_tablero.append(ficha_central_control)
            
            # Añadir fichas de abajo
            for datos_ficha in self.datos_fichas_abajo:
                if datos_ficha["es_doble"]:
                    ficha_control = crear_ficha_visual_horizontal(
                        datos_ficha["numero1"], datos_ficha["numero2"],
                        repr1=datos_ficha["repr1"], repr2=datos_ficha["repr2"],
                        es_computadora=datos_ficha["es_computadora"],
                        es_central=datos_ficha["es_central"]
                    )
                else:
                    ficha_control = crear_ficha_visual(
                        datos_ficha["numero1"], datos_ficha["numero2"],
                        repr1=datos_ficha["repr1"], repr2=datos_ficha["repr2"],
                        es_computadora=datos_ficha["es_computadora"],
                        es_central=datos_ficha["es_central"]
                    )
                controles_tablero.append(ficha_control)

            if len(controles_tablero) == 1:
                controles_tablero.insert(0, ft.Text(
                    "Solo está la ficha central",
                    size=14,
                    color=colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ))

            # Crear overlay en lugar de diálogo
            overlay_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text("Tablero Completo", size=20, weight=ft.FontWeight.BOLD, color=colors.WHITE),
                                    ft.IconButton(
                                        icon=ft.icons.CLOSE,
                                        icon_color=colors.WHITE,
                                        on_click=lambda _: self.cerrar_overlay()
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            bgcolor=colors.BLUE_600,
                            padding=10,
                            border_radius=ft.border_radius.only(top_left=10, top_right=10)
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=controles_tablero,
                                scroll=ft.ScrollMode.AUTO,
                                spacing=5,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=280,
                            height=400,
                            bgcolor=colors.WHITE,
                            padding=10
                        )
                    ],
                    spacing=0
                ),
                bgcolor=colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.BLACK26,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                )
            )

            # Crear contenedor de fondo semi-transparente
            overlay_background = ft.Container(
                content=ft.Stack(
                    [
                        ft.Container(
                            bgcolor=colors.BLACK54,
                            expand=True,
                            on_click=lambda _: self.cerrar_overlay()
                        ),
                        ft.Container(
                            content=overlay_content,
                            alignment=ft.alignment.center,
                            expand=True
                        )
                    ]
                ),
                expand=True
            )

            # Añadir overlay a la página
            self.page.overlay.append(overlay_background)
            self.overlay_actual = overlay_background
            self.page.update()
            
            print("=== DEBUG: Overlay mostrado ===")
            
        except Exception as ex:
            print(f"=== DEBUG: Error en overlay: {ex} ===")

    def cerrar_overlay(self):
        """Cierra el overlay del tablero"""
        print("=== DEBUG: Cerrando overlay ===")
        try:
            if hasattr(self, 'overlay_actual') and self.overlay_actual:
                self.page.overlay.remove(self.overlay_actual)
                self.overlay_actual = None
                self.page.update()
                print("=== DEBUG: Overlay cerrado ===")
        except Exception as ex:
            print(f"=== DEBUG: Error cerrando overlay: {ex} ===")

    def jugador_pasa_turno(self, e):
        if not self.turno_jugador:
            # Not player's turn, do nothing or show a message
            self.mostrar_mensaje("No es tu turno.")
            return

        # Player chooses to pass.
        self.mostrar_mensaje("Has decidido pasar el turno.")
        
        self.turno_jugador = False
        self.actualizar_indicador_turno() # Update indicator to "Turno PC"
        self.page.update() # Ensure UI reflects the change

        # Trigger AI's turn after a short delay
        threading.Timer(1.0, self.colocar_ficha_especial).start()

    def test_boton_simple(self, e):
        """Método de prueba simple para verificar que el botón funciona"""
        print("¡BOTÓN FUNCIONA!")
        
        # Probar con SnackBar en lugar de diálogo
        snack_bar = ft.SnackBar(
            content=ft.Text("¡El botón Ver Tablero funciona correctamente!", color=colors.WHITE),
            bgcolor=colors.GREEN_600,
            duration=3000
        )
        
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
        
        print("SnackBar mostrado")
        
        # También intentar cambiar el título temporalmente
        titulo_original = self.titulo.value
        self.titulo.value = "¡BOTÓN FUNCIONA!"
        self.titulo.color = colors.GREEN
        self.page.update()
        
        # Restaurar título después de 2 segundos
        def restaurar_titulo():
            time.sleep(2)
            self.titulo.value = titulo_original
            self.titulo.color = colors.BLACK
            self.page.update()
        
        threading.Thread(target=restaurar_titulo, daemon=True).start()

    def colocar_ficha_especial(self, e=None):
        self.turno_jugador = False
        self.game_timer.stop()

        if self.turno_jugador:
            self.game_timer.start()
            return

        numero_arriba = self.estado_juego.numero_arriba
        numero_abajo = self.estado_juego.numero_abajo
        
        fichas_jugables_arriba = []
        fichas_jugables_abajo = []
        
        for ficha in self.fichas_app:
            if ficha.numero1 == numero_arriba or ficha.numero2 == numero_arriba:
                fichas_jugables_arriba.append((ficha, "app"))
            if ficha.numero1 == numero_abajo or ficha.numero2 == numero_abajo:
                fichas_jugables_abajo.append((ficha, "app"))
        
        for ficha in self.pozo:
            if ficha.numero1 == numero_arriba or ficha.numero2 == numero_arriba:
                fichas_jugables_arriba.append((ficha, "pozo"))
            if ficha.numero1 == numero_abajo or ficha.numero2 == numero_abajo:
                fichas_jugables_abajo.append((ficha, "pozo"))
        
        todas_fichas_jugables = fichas_jugables_arriba + fichas_jugables_abajo
        
        if not todas_fichas_jugables:
            if self.pozo:
                ficha_nueva = self.pozo.pop(0)
                self.fichas_app.append(ficha_nueva)
                self.fichas_app_view.controls.append(
                    ft.Container(
                        width=60,
                        height=120,
                        bgcolor=colors.BROWN,
                        border_radius=5
                    )
                )
                for container in self.pozo_view.controls:
                    if hasattr(container, 'actualizar'):
                        container.actualizar()
                
                mensaje = f"La computadora ha tomado una ficha del pozo. Quedan {len(self.pozo)} fichas"
                self.mostrar_mensaje(mensaje)
                self.page.update()
                return
            else:
                mensaje = "La computadora no tiene fichas para jugar y el pozo está vacío. Pasa."
                self.game_timer.stop()
                self.mostrar_mensaje(mensaje)
                return
        
        ficha_elegida, origen = random.choice(todas_fichas_jugables)
        
        if (ficha_elegida, origen) in fichas_jugables_arriba:
            lado_a_jugar = "arriba"
            if ficha_elegida.numero1 == numero_arriba:
                ficha_elegida.numero1, ficha_elegida.numero2 = ficha_elegida.numero2, ficha_elegida.numero1
                ficha_elegida.repr1, ficha_elegida.repr2 = ficha_elegida.repr2, ficha_elegida.repr1
            self.estado_juego.numero_arriba = ficha_elegida.numero1
        else:
            lado_a_jugar = "abajo"
            if ficha_elegida.numero2 == numero_abajo:
                ficha_elegida.numero1, ficha_elegida.numero2 = ficha_elegida.numero2, ficha_elegida.numero1
                ficha_elegida.repr1, ficha_elegida.repr2 = ficha_elegida.repr2, ficha_elegida.repr1
            self.estado_juego.numero_abajo = ficha_elegida.numero2
        
        if origen == "app":
            self.fichas_app.remove(ficha_elegida)
            if self.fichas_app_view.controls:
                self.fichas_app_view.controls.pop()
        else:
            self.pozo.remove(ficha_elegida)
            for container in self.pozo_view.controls:
                if hasattr(container, 'actualizar'):
                    container.actualizar()
        
        ficha_elegida.repr1 = self.obtener_representacion_forzada(ficha_elegida.numero1, False)
        ficha_elegida.repr2 = self.obtener_representacion_forzada(ficha_elegida.numero2, False)
        
        es_doble = ficha_elegida.numero1 == ficha_elegida.numero2
        
        ficha_visual = (
            crear_ficha_visual_horizontal(ficha_elegida.numero1, ficha_elegida.numero2, 
                                          repr1=ficha_elegida.repr1, repr2=ficha_elegida.repr2,
                                          es_computadora=True)
            if es_doble else
            crear_ficha_visual(ficha_elegida.numero1, ficha_elegida.numero2, 
                               repr1=ficha_elegida.repr1, repr2=ficha_elegida.repr2,
                               es_computadora=True)
        )
        
        # Guardar datos para el diálogo
        datos_ficha = {
            "numero1": ficha_elegida.numero1,
            "numero2": ficha_elegida.numero2,
            "repr1": ficha_elegida.repr1,
            "repr2": ficha_elegida.repr2,
            "es_doble": es_doble,
            "es_computadora": True,
            "es_central": False
        }
        
        if lado_a_jugar == "arriba":
            self.datos_fichas_arriba.insert(0, datos_ficha)  # Guardar datos para diálogo
            indices_zonas = [i for i, control in enumerate(self.area_juego.controls) 
                            if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[0]
                self.area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = self.crear_zona_destino("arriba")
                self.area_juego.controls.insert(0, nueva_zona)
                self.area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        else:
            self.datos_fichas_abajo.append(datos_ficha)  # Guardar datos para diálogo
            indices_zonas = [i for i, control in enumerate(self.area_juego.controls) 
                            if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[-1]
                self.area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = self.crear_zona_destino("abajo")
                self.area_juego.controls.append(nueva_zona)
                self.area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        if len(self.fichas_app) == 0:
            mensaje = "¡La computadora ha ganado!"
            self.mostrar_mensaje(mensaje)
        else:
            self.turno_jugador = True
            self.actualizar_indicador_turno()
        
        origen_texto = "el pozo" if origen == "pozo" else "su mano"
        if origen == "pozo":
            mensaje = f"La computadora ha jugado una ficha del pozo. Quedan {len(self.pozo)} fichas"
        else:
            mensaje = "La computadora ha jugado una ficha de su mano"
        self.mostrar_mensaje(mensaje)
        
        self.actualizar_vista_extremos()
        self.actualizar_zoom_automatico()
        
        self.game_timer.start()
        self.page.update()

    def actualizar_indicador_turno(self):
        if self.turno_jugador:
            self.indicador_turno.bgcolor = colors.GREEN
            self.texto_turno.value = "Tu turno"
        else:
            self.indicador_turno.bgcolor = colors.RED
            self.texto_turno.value = "Turno PC"
        self.page.update()

    def obtener_representacion_forzada(self, numero, es_para_jugador):
        color, _ = COLORES_DOMINO[numero]
        if self.modo_central_numeros:
            return ("numero", str(numero)) if not es_para_jugador else ("color", color)
        else:
            return ("color", color) if not es_para_jugador else ("numero", str(numero))

    def convertir_fichas_segun_modo(self, fichas, es_para_jugador):
        for ficha in fichas:
            ficha.repr1 = self.obtener_representacion_forzada(ficha.numero1, es_para_jugador)
            ficha.repr2 = self.obtener_representacion_forzada(ficha.numero2, es_para_jugador)
        return fichas

    def get_mensaje_ficha_inicial(self, quien_empieza, ficha, usa_numeros_central):
        quien_txt = 'Tú empiezas' if quien_empieza == "jugador" else 'La computadora empieza'
        
        if usa_numeros_central:
            return f"{quien_txt} con la ficha [{ficha.numero1}-{ficha.numero2}]"
        else:
            _, nombre_color1 = COLORES_DOMINO[ficha.numero1]
            _, nombre_color2 = COLORES_DOMINO[ficha.numero2]
            return f"{quien_txt} con la ficha [{nombre_color1}-{nombre_color2}]"

    def crear_zona_destino(self, posicion):
        def on_accept(e):
            if not self.turno_jugador:
                return False
                
            ficha = self.page.get_control(e.src_id).data
            
            if posicion == "arriba":
                numero_a_comparar = self.estado_juego.numero_arriba
                numero_valido = ficha.numero2 == numero_a_comparar
                if numero_valido:
                    self.estado_juego.numero_arriba = ficha.numero1
            else:
                numero_a_comparar = self.estado_juego.numero_abajo
                numero_valido = ficha.numero1 == numero_a_comparar
                if numero_valido:
                    self.estado_juego.numero_abajo = ficha.numero2
            
            if numero_valido:
                # Remover la ficha de la vista del jugador antes de procesarla
                for control in self.fichas_jugador_view.controls[:]:
                    if control.data.identificador == ficha.identificador:
                        self.fichas_jugador_view.controls.remove(control)
                        break

                self.estado_juego.fichas_jugadas.append(ficha)
                
                # Asegurar la representación correcta según el modo
                ficha.repr1 = self.obtener_representacion_forzada(ficha.numero1, False)
                ficha.repr2 = self.obtener_representacion_forzada(ficha.numero2, False)
                
                es_doble = ficha.numero1 == ficha.numero2
                ficha_visual = (
                    crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2, 
                                               repr1=ficha.repr1, repr2=ficha.repr2)
                    if es_doble
                    else crear_ficha_visual(ficha.numero1, ficha.numero2, 
                                         repr1=ficha.repr1, repr2=ficha.repr2)
                )
                
                if posicion == "arriba":
                    self.datos_fichas_arriba.insert(0, {  # Guardar datos para diálogo
                        "numero1": ficha.numero1,
                        "numero2": ficha.numero2,
                        "repr1": ficha.repr1,
                        "repr2": ficha.repr2,
                        "es_doble": es_doble,
                        "es_computadora": False,
                        "es_central": False
                    })
                    indices_zonas = [i for i, control in enumerate(self.area_juego.controls) 
                                   if isinstance(control, ft.DragTarget)]
                    if indices_zonas:
                        indice_actual = indices_zonas[0]
                        self.area_juego.controls[indice_actual] = ficha_visual
                        nueva_zona = self.crear_zona_destino("arriba")
                        self.area_juego.controls.insert(0, nueva_zona)
                        self.area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER
                else:
                    self.datos_fichas_abajo.append({  # Guardar datos para diálogo
                        "numero1": ficha.numero1,
                        "numero2": ficha.numero2,
                        "repr1": ficha.repr1,
                        "repr2": ficha.repr2,
                        "es_doble": es_doble,
                        "es_computadora": False,
                        "es_central": False
                    })
                    indices_zonas = [i for i, control in enumerate(self.area_juego.controls) 
                                   if isinstance(control, ft.DragTarget)]
                    if indices_zonas:
                        indice_actual = indices_zonas[-1]
                        self.area_juego.controls[indice_actual] = ficha_visual
                        nueva_zona = self.crear_zona_destino("abajo")
                        self.area_juego.controls.append(nueva_zona)
                        self.area_juego.horizontal_alignment = ft.CrossAxisAlignment.CENTER

                self.turno_jugador = False
                self.actualizar_indicador_turno()
                self.actualizar_vista_extremos()
                self.actualizar_zoom_automatico()
                
                if len(self.fichas_jugador_view.controls) == 0:
                    mensaje = "¡Has ganado!"
                    self.mostrar_mensaje(mensaje)
                elif not self.turno_jugador:
                    threading.Timer(2.0, self.colocar_ficha_especial).start()
                
                self.page.update()
                return True
            return False

        return ft.DragTarget(
            content=ft.Container(
                width=50,
                height=100,
                border=ft.border.all(2, colors.GREY_400),
                border_radius=5,
                bgcolor="#E0E0E033",
                content=ft.Column(
                    controls=[
                        ft.Container(
                            height=50,
                            width=50,
                            border=ft.border.all(1, colors.GREY_400)
                        ),
                        ft.Container(
                            height=50,
                            width=50,
                            border=ft.border.all(1, colors.GREY_400)
                        )
                    ],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
                )
            ),
            on_accept=on_accept
        )

def configurar_ventana_domino(page: ft.Page, volver_al_menu_principal):
    juego = JuegoPrincipiante(page, volver_al_menu_principal)





