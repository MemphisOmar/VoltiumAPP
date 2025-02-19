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
    if not fichas_disponibles:
        fichas_disponibles = crear_fichas_domino()
    
    # Repartir 7 fichas para el jugador (cambiado de 8 a 7)
    fichas_jugador = []
    for _ in range(7):
        ficha = random.choice(fichas_disponibles)
        fichas_jugador.append(ficha)
        fichas_disponibles.remove(ficha)
    
    # Repartir 7 fichas para la aplicación
    fichas_app = []
    for _ in range(7):
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
            border_radius=20,  
            border=ft.border.all(0.5, colors.BLACK)  # Borde negro delgado
        )

def crear_ficha_visual(numero1, numero2, es_central=False, repr1=None, repr2=None):
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    
    # Usar representaciones pasadas o generar nuevas si no se proporcionaron
    repr1 = repr1 or obtener_representacion_valor(numero1)
    repr2 = repr2 or obtener_representacion_valor(numero2)
    
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(repr1),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(repr2),
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

def crear_ficha_visual_horizontal(numero1, numero2, es_central=False, repr1=None, repr2=None):
    """Crea una ficha visual en orientación horizontal"""
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    
    repr1 = repr1 or obtener_representacion_valor(numero1)
    repr2 = repr2 or obtener_representacion_valor(numero2)
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(repr1),
                    alignment=ft.alignment.center,
                    bgcolor=color_fondo,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(repr2),
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
                        content=crear_contenido_ficha(ficha.repr1),
                        alignment=ft.alignment.center,
                        bgcolor=colors.WHITE,
                        width=60,
                        height=60,
                        border=ft.border.all(1, colors.BLACK)
                    ),
                    ft.Container(
                        content=crear_contenido_ficha(ficha.repr2),
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
        # Intercambiar los números y sus representaciones
        ficha.numero1, ficha.numero2 = ficha.numero2, ficha.numero1
        ficha.repr1, ficha.repr2 = ficha.repr2, ficha.repr1
        # Actualizar la visualización
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
                ficha_visual = crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2, repr1=ficha.repr1, repr2=ficha.repr2)
            else:
                ficha_visual = crear_ficha_visual(ficha.numero1, ficha.numero2, repr1=ficha.repr1, repr2=ficha.repr2)
            
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
                    content=crear_contenido_ficha(ficha.repr1),
                    alignment=ft.alignment.center,
                    bgcolor=colors.WHITE,
                    width=60,
                    height=60,
                    border=ft.border.all(1, colors.BLACK)
                ),
                ft.Container(
                    content=crear_contenido_ficha(ficha.repr2),
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
    """Crea una columna de fichas ocultas para el pozo"""
    texto_pozo = ft.Text(f"Pozo ({len(fichas)})", size=20, color=colors.BLACK)
    columna_fichas = None

    def actualizar_vista_pozo():
        """Actualiza el contador y las fichas visuales del pozo"""
        texto_pozo.value = f"Pozo ({len(fichas)})"
        if len(columna_fichas.controls) > len(fichas):
            columna_fichas.controls.pop()

    def on_ficha_click(e, ficha):
        if ficha in fichas:
            on_ficha_seleccionada(ficha)
            actualizar_vista_pozo()
            e.control.page.update()

    # Crear las fichas ocultas con más espacio entre ellas
    columna_fichas = ft.Column(
        controls=[
            ft.Container(
                width=80,  # Aumentado de 60 a 80
                height=140,  # Aumentado de 120 a 140
                bgcolor=colors.BROWN,
                border_radius=5,
                border=ft.border.all(1, colors.BLACK),
                margin=ft.margin.only(bottom=5),  # Agregar margen entre fichas
                on_click=lambda e, f=ficha: on_ficha_click(e, f)
            ) 
            for ficha in fichas
        ],
        spacing=2,
        scroll=ft.ScrollMode.AUTO,
        height=600  # Altura fija para la columna de fichas
    )
    
    return ft.Column(
        controls=[
            texto_pozo,
            ft.Container(
                content=columna_fichas,
                width=120,  # Ancho fijo para el contenedor
                height=600,  # Aumentado de 300 a 600
                border=ft.border.all(1, colors.GREY_400),
                border_radius=5,
                padding=10
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

def encontrar_ficha_inicial(fichas_jugador, fichas_app):
    """
    Determina quién tiene la ficha más alta y cuál es esa ficha.
    Prioriza dobles y luego suma de números.
    Retorna: (ficha, "jugador"/"app")
    """
    def valor_ficha(ficha):
        # Priorizar dobles
        if ficha.numero1 == ficha.numero2:
            return (1, ficha.numero1, ficha.numero2)  # (es_doble, primer_numero, segundo_numero)
        # Para no dobles, ordenar por suma de números
        return (0, max(ficha.numero1, ficha.numero2), min(ficha.numero1, ficha.numero2))
    
    mejor_ficha_jugador = max(fichas_jugador, key=valor_ficha)
    mejor_ficha_app = max(fichas_app, key=valor_ficha)
    
    if valor_ficha(mejor_ficha_jugador) > valor_ficha(mejor_ficha_app):
        return mejor_ficha_jugador, "jugador"
    return mejor_ficha_app, "app"

def configurar_ventana_domino(page: ft.Page, volver_al_menu_principal):
    # Determinar aleatoriamente el modo de juego
    modo_maquina_colores = random.choice([True, False])
    
    # Definir el mensaje según el modo
    modo_mensaje = ("Jugarás con números y la máquina con colores" 
                   if modo_maquina_colores else 
                   "Jugarás con colores y la máquina con números")

    def obtener_representacion_forzada(numero, es_para_jugador):
        """Fuerza la representación según el modo de juego"""
        color, _ = COLORES_DOMINO[numero]
        if modo_maquina_colores:
            # Máquina usa colores, jugador usa números
            return ("color", color) if not es_para_jugador else ("numero", str(numero))
        else:
            # Máquina usa números, jugador usa colores
            return ("numero", str(numero)) if not es_para_jugador else ("color", color)

    def convertir_fichas_segun_modo(fichas, es_para_jugador):
        """Convierte todas las fichas al modo correspondiente"""
        for ficha in fichas:
            ficha.repr1 = obtener_representacion_forzada(ficha.numero1, es_para_jugador)
            ficha.repr2 = obtener_representacion_forzada(ficha.numero2, es_para_jugador)
        return fichas

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
    fichas_jugador, fichas_app, pozo = repartir_fichas()
    
    # Convertir las fichas según el modo
    fichas_jugador = convertir_fichas_segun_modo(fichas_jugador, True)
    fichas_app = convertir_fichas_segun_modo(fichas_app, False)
    
    # Determinar ficha central y quién empieza
    ficha_central, quien_empieza = encontrar_ficha_inicial(fichas_jugador, fichas_app)
    
    # Remover la ficha central de quien la tenía
    if quien_empieza == "jugador":
        fichas_jugador.remove(ficha_central)
    else:
        fichas_app.remove(ficha_central)
    
    estado_juego = EstadoJuego(ficha_central)

    def cerrar_dialogo(e):
        dlg.open = False
        page.update()

    # Mostrar mensaje del modo de juego más compacto
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
                            f"{'Tú empiezas' if quien_empieza == 'jugador' else 'La computadora empieza'} "
                            f"con la ficha [{ficha_central.numero1}-{ficha_central.numero2}]",
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
                on_click=cerrar_dialogo,  # Cambiado para usar la nueva función
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

    def on_ficha_jugada(ficha, lado):
        # Remover la ficha jugada de la mano del jugador
        for control in fichas_jugador_view.controls[:]:
            if control.data.identificador == ficha.identificador:
                fichas_jugador_view.controls.remove(control)
                break
        page.update()

    def agregar_ficha_del_pozo(ficha):
        """Función que se llama cuando se selecciona una ficha del pozo"""
        if ficha in pozo:  # Verificar que la ficha aún está en el pozo
            pozo.remove(ficha)  # Primero remover la ficha del pozo
            # Convertir la ficha al modo del jugador antes de agregarla
            ficha.repr1 = obtener_representacion_forzada(ficha.numero1, True)
            ficha.repr2 = obtener_representacion_forzada(ficha.numero2, True)
            fichas_jugador.append(ficha)  # Luego agregarla al jugador
            fichas_jugador_view.controls.append(crear_ficha_visual_jugador(ficha))
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
    
    # Determinar si la ficha central es doble
    es_ficha_central_doble = ficha_central.numero1 == ficha_central.numero2
    
    # Crear ficha central visual según si es doble o no
    ficha_central_visual = (
        crear_ficha_visual_horizontal(ficha_central.numero1, ficha_central.numero2, es_central=True, repr1=ficha_central.repr1, repr2=ficha_central.repr2)
        if es_ficha_central_doble
        else crear_ficha_visual(ficha_central.numero1, ficha_central.numero2, es_central=True, repr1=ficha_central.repr1, repr2=ficha_central.repr2)
    )

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
                        width=140,  # Aumentado de 100 a 140
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