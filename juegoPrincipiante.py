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
    # Asegurarnos de que las fichas estén inicializadas
    if not fichas_disponibles:
        fichas_disponibles = crear_fichas_domino()
    
    # Crear una copia de las fichas disponibles para manipular
    fichas_temp = fichas_disponibles.copy()
    
    # Repartir 7 fichas para el jugador
    fichas_jugador = []
    for _ in range(7):
        if not fichas_temp:  # Si se acabaron las fichas, crear nuevas
            fichas_temp = crear_fichas_domino()
        ficha = random.choice(fichas_temp)
        fichas_jugador.append(ficha)
        fichas_temp.remove(ficha)
    
    # Repartir 7 fichas para la aplicación
    fichas_app = []
    for _ in range(7):
        if not fichas_temp:  # Si se acabaron las fichas, crear nuevas
            fichas_temp = crear_fichas_domino()
        ficha = random.choice(fichas_temp)
        fichas_app.append(ficha)
        fichas_temp.remove(ficha)
    
    # Las fichas restantes serán el pozo
    pozo = fichas_temp.copy() if fichas_temp else []
    
    # Si el pozo está vacío, crear algunas fichas adicionales
    if not pozo:
        pozo_adicional = crear_fichas_domino()
        # Eliminar las fichas que ya tiene el jugador o la aplicación
        ids_asignados = [f.identificador for f in fichas_jugador + fichas_app]
        pozo = [f for f in pozo_adicional if f.identificador not in ids_asignados]
    
    # Actualizar las fichas disponibles globales (quitar las que se repartieron)
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
            else:
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[-1]
                    area_juego.controls[indice_actual] = ficha_visual
                    nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                    area_juego.controls.append(nueva_zona)
            
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

def configurar_ventana_domino(page: ft.Page, volver_al_menu_principal):
    global fichas_disponibles
    fichas_disponibles = crear_fichas_domino()
    
    modo_central_numeros = random.choice([True, False])
    
    modo_mensaje = ("El tablero central mostrará números y tus fichas colores" 
                   if modo_central_numeros else 
                   "El tablero central mostrará colores y tus fichas números")

    escala_actual = 1.0

    def obtener_representacion_forzada(numero, es_para_jugador):
        color, _ = COLORES_DOMINO[numero]
        if modo_central_numeros:
            return ("numero", str(numero)) if not es_para_jugador else ("color", color)
        else:
            return ("color", color) if not es_para_jugador else ("numero", str(numero))

    def convertir_fichas_segun_modo(fichas, es_para_jugador):
        for ficha in fichas:
            ficha.repr1 = obtener_representacion_forzada(ficha.numero1, es_para_jugador)
            ficha.repr2 = obtener_representacion_forzada(ficha.numero2, es_para_jugador)
        return fichas

    def volver_al_menu_principal_click(e):
        global fichas_disponibles
        fichas_disponibles = crear_fichas_domino()
        volver_al_menu_principal(page)

    def get_mensaje_ficha_inicial(quien_empieza, ficha, usa_numeros_central):
        quien_txt = 'Tú empiezas' if quien_empieza == "jugador" else 'La computadora empieza'
        
        if usa_numeros_central:
            return f"{quien_txt} con la ficha [{ficha.numero1}-{ficha.numero2}]"
        else:
            _, nombre_color1 = COLORES_DOMINO[ficha.numero1]
            _, nombre_color2 = COLORES_DOMINO[ficha.numero2]
            return f"{quien_txt} con la ficha [{nombre_color1}-{nombre_color2}]"

    page.clean()
    page.title = "DOMINO - Principiante"
    page.bgcolor = "#1B4D3E"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.margin = 0

    titulo = ft.Text("Modo Principiante", size=24, color=colors.BLACK)
    volver_button = ft.ElevatedButton(
        text="Volver al menú",
        on_click=volver_al_menu_principal_click,
        width=120,
        height=40
    )

    fichas_jugador, fichas_app, pozo = repartir_fichas()
    
    fichas_jugador = convertir_fichas_segun_modo(fichas_jugador, True)
    fichas_app = convertir_fichas_segun_modo(fichas_app, False)
    
    ficha_central, quien_empieza = encontrar_ficha_inicial(fichas_jugador, fichas_app)
    
    if quien_empieza == "jugador":
        fichas_jugador.remove(ficha_central)
    else:
        fichas_app.remove(ficha_central)
    
    ficha_central.repr1 = obtener_representacion_forzada(ficha_central.numero1, False)
    ficha_central.repr2 = obtener_representacion_forzada(ficha_central.numero2, False)
    
    estado_juego = EstadoJuego(ficha_central)

    def cerrar_dialogo(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
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
                            modo_mensaje,
                            size=14,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=ft.padding.all(5)
                    ),
                    ft.Divider(height=1, color=colors.BLUE_GREY_200),
                    ft.Container(
                        content=ft.Text(
                            get_mensaje_ficha_inicial(quien_empieza, ficha_central, modo_central_numeros),
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
                on_click=cerrar_dialogo,
                style=ft.ButtonStyle(
                    color=colors.WHITE,
                    bgcolor=colors.BLUE_400
                )
            )
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=8)
    )
    page.dialog = dlg
    dlg.open = True

    def calcular_zoom_automatico(area_juego):
        num_fichas = len([c for c in area_juego.controls if not isinstance(c, ft.DragTarget)])
        
        if num_fichas <= 3:
            return 0.95
        elif num_fichas <= 6:
            return 0.7
        elif num_fichas <= 9:
            return 0.55
        elif num_fichas <= 12:
            return 0.40
        else:
            return 0.6

    def actualizar_zoom_automatico(area_juego, contenedor_area_juego, texto_zoom):
        nuevo_zoom = calcular_zoom_automatico(area_juego)
        contenedor_area_juego.scale = nuevo_zoom
        texto_zoom.value = f"{int(nuevo_zoom * 100)}%"
        contenedor_area_juego.page.update()

    def on_ficha_jugada(ficha, lado):
        for control in fichas_jugador_view.controls[:]:
            if control.data.identificador == ficha.identificador:
                fichas_jugador_view.controls.remove(control)
                break
        
        es_doble = ficha.numero1 == ficha.numero2
        
        ficha_visual = (
            crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2, 
                                       repr1=ficha.repr1, repr2=ficha.repr2)
            if es_doble
            else crear_ficha_visual(ficha.numero1, ficha.numero2, 
                                  repr1=ficha.repr1, repr2=ficha.repr2)
        )
        
        if lado == "arriba":
            indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                           if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[0]
                area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                area_juego.controls.insert(0, nueva_zona)
        else:
            indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                           if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[-1]
                area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                area_juego.controls.append(nueva_zona)
        
        actualizar_zoom_automatico(area_juego, contenedor_area_juego, texto_zoom)
        page.update()

        page.after(3000, lambda _: colocar_ficha_especial())

    def agregar_ficha_del_pozo(ficha):
        if ficha in pozo:
            pozo.remove(ficha)
            ficha.repr1 = obtener_representacion_forzada(ficha.numero1, True)
            ficha.repr2 = obtener_representacion_forzada(ficha.numero2, True)
            fichas_jugador.append(ficha)
            fichas_jugador_view.controls.append(crear_ficha_visual_jugador(ficha))
            page.update()

    def mostrar_mensaje(page, mensaje):
        dlg = ft.AlertDialog(
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("OK", on_click=lambda e: cerrar_mensaje(e, dlg))
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def cerrar_mensaje(e, dlg):
        dlg.open = False
        e.page.update()
    
    def aumentar_zoom(e):
        nonlocal escala_actual
        if escala_actual < 2.0:
            escala_actual += 0.1
            actualizar_zoom()
            
    def disminuir_zoom(e):
        nonlocal escala_actual
        if escala_actual > 0.5:
            escala_actual -= 0.1
            actualizar_zoom()
            
    def restablecer_zoom(e):
        nonlocal escala_actual
        escala_actual = 1.0
        actualizar_zoom()
        
    def actualizar_zoom():
        contenedor_area_juego.scale = escala_actual
        texto_zoom.value = f"{int(escala_actual * 100)}%"
        page.update()

    def colocar_ficha_especial(e=None):
        numero_arriba = estado_juego.numero_arriba
        numero_abajo = estado_juego.numero_abajo
        
        fichas_jugables_arriba = []
        fichas_jugables_abajo = []
        
        for ficha in fichas_app:
            if ficha.numero1 == numero_arriba or ficha.numero2 == numero_arriba:
                fichas_jugables_arriba.append((ficha, "app"))
            if ficha.numero1 == numero_abajo or ficha.numero2 == numero_abajo:
                fichas_jugables_abajo.append((ficha, "app"))
        
        for ficha in pozo:
            if ficha.numero1 == numero_arriba or ficha.numero2 == numero_arriba:
                fichas_jugables_arriba.append((ficha, "pozo"))
            if ficha.numero1 == numero_abajo or ficha.numero2 == numero_abajo:
                fichas_jugables_abajo.append((ficha, "pozo"))
        
        todas_fichas_jugables = fichas_jugables_arriba + fichas_jugables_abajo
        
        if not todas_fichas_jugables:
            if pozo:
                ficha_nueva = pozo.pop(0)
                fichas_app.append(ficha_nueva)
                fichas_app_view.controls.append(
                    ft.Container(
                        width=60,
                        height=120,
                        bgcolor=colors.BROWN,
                        border_radius=5
                    )
                )
                for container in pozo_view.controls:
                    if hasattr(container, 'actualizar'):
                        container.actualizar()
                
                mensaje = "La computadora ha tomado una ficha del pozo"
                mostrar_mensaje(page, mensaje)
                page.update()
                return
            else:
                mensaje = "La computadora no tiene fichas para jugar y el pozo está vacío. Pasa."
                mostrar_mensaje(page, mensaje)
                return
        
        ficha_elegida, origen = random.choice(todas_fichas_jugables)
        
        if (ficha_elegida, origen) in fichas_jugables_arriba:
            lado_a_jugar = "arriba"
            if ficha_elegida.numero1 == numero_arriba:
                ficha_elegida.numero1, ficha_elegida.numero2 = ficha_elegida.numero2, ficha_elegida.numero1
                ficha_elegida.repr1, ficha_elegida.repr2 = ficha_elegida.repr2, ficha_elegida.repr1
            estado_juego.numero_arriba = ficha_elegida.numero1
        else:
            lado_a_jugar = "abajo"
            if ficha_elegida.numero2 == numero_abajo:
                ficha_elegida.numero1, ficha_elegida.numero2 = ficha_elegida.numero2, ficha_elegida.numero1
                ficha_elegida.repr1, ficha_elegida.repr2 = ficha_elegida.repr2, ficha_elegida.repr1
            estado_juego.numero_abajo = ficha_elegida.numero2
        
        if origen == "app":
            fichas_app.remove(ficha_elegida)
            if fichas_app_view.controls:
                fichas_app_view.controls.pop()
        else:
            pozo.remove(ficha_elegida)
            for container in pozo_view.controls:
                if hasattr(container, 'actualizar'):
                    container.actualizar()
        
        ficha_elegida.repr1 = obtener_representacion_forzada(ficha_elegida.numero1, False)
        ficha_elegida.repr2 = obtener_representacion_forzada(ficha_elegida.numero2, False)
        
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
        
        if lado_a_jugar == "arriba":
            indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                            if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[0]
                area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                area_juego.controls.insert(0, nueva_zona)
            else:
                mensaje = "Error: No hay zonas disponibles para colocar la ficha"
                mostrar_mensaje(page, mensaje)
                return
            
        else:
            indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                            if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[-1]
                area_juego.controls[indice_actual] = ficha_visual
                nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                area_juego.controls.append(nueva_zona)
            else:
                mensaje = "Error: No hay zonas disponibles para colocar la ficha"
                mostrar_mensaje(page, mensaje)
                return
        
        if len(fichas_app) == 0:
            mensaje = "¡La computadora ha ganado!"
            mostrar_mensaje(page, mensaje)
        
        origen_texto = "el pozo" if origen == "pozo" else "su mano"
        mensaje = f"La computadora ha jugado una ficha de {origen_texto}"
        mostrar_mensaje(page, mensaje)
        
        actualizar_zoom_automatico(area_juego, contenedor_area_juego, texto_zoom)
        page.update()

    area_juego = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
        scroll=ft.ScrollMode.AUTO,
        height=700,
    )

    zona_arriba = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
    zona_abajo = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
    
    es_ficha_central_doble = ficha_central.numero1 == ficha_central.numero2
    
    ficha_central_visual = (
        crear_ficha_visual_horizontal(ficha_central.numero1, ficha_central.numero2, es_central=True, repr1=ficha_central.repr1, repr2=ficha_central.repr2)
        if es_ficha_central_doble
        else crear_ficha_visual(ficha_central.numero1, ficha_central.numero2, es_central=True, repr1=ficha_central.repr1, repr2=ficha_central.repr2)
    )

    area_juego.controls = [
        zona_arriba,
        ficha_central_visual,
        zona_abajo
    ]

    contenedor_area_juego = ft.Container(
        content=area_juego,
        height=600,
        border=ft.border.all(1, colors.GREY_400),
        border_radius=5,
        padding=5,
        scale=escala_actual,
        alignment=ft.alignment.center,
        bgcolor="#1B4D3E"  
    )
    
    texto_zoom = ft.Text("100%", size=14, weight=ft.FontWeight.BOLD)
    
    controles_zoom = ft.Row(
        [texto_zoom],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
    )

    fichas_jugador_view = crear_fichas_jugador_row(fichas_jugador, estado_juego, page)
    fichas_app_view = crear_fichas_app_row(len(fichas_app))
    pozo_view = crear_pozo_column(pozo, agregar_ficha_del_pozo)

    boton_jugar_oponente = ft.ElevatedButton(
        text="Jugar oponente",
        tooltip="Hacer jugar al oponente",
        on_click=colocar_ficha_especial,
        width=120,
        height=40,
        style=ft.ButtonStyle(
            color=colors.WHITE,
            bgcolor=colors.BLUE_700
        )
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                pozo_view,
                                volver_button
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
                                titulo,
                                ft.Container(
                                    content=fichas_app_view,
                                    padding=2,
                                    height=100,
                                ),
                                ft.Container(
                                    content=boton_jugar_oponente,
                                    alignment=ft.alignment.center,
                                    padding=5,
                                ),
                                contenedor_area_juego,
                                controles_zoom,
                                ft.Container(
                                    content=fichas_jugador_view,
                                    padding=2,
                                    height=150,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
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
        )
    )

    actualizar_zoom_automatico(area_juego, contenedor_area_juego, texto_zoom)
    page.update()





