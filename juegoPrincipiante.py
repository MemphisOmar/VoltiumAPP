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
    if tipo == "numero":
        # En lugar de mostrar el número como texto, mostrar puntos
        return crear_representacion_puntos(int(valor))
    else:  # tipo == "color"
        # En lugar de un círculo, llenar toda la mitad de la ficha con el color
        return ft.Container(
            width=60,  # Ancho completo de la mitad de la ficha
            height=60,  # Alto completo de la mitad de la ficha
            bgcolor=valor,
            # No usamos border_radius para que sea rectangular, no circular
            # Mantenemos un borde negro para la consistencia visual
            border=ft.border.all(0.5, colors.BLACK)
        )

# Añadir un parámetro para el color del borde
def crear_ficha_visual(numero1, numero2, es_central=False, repr1=None, repr2=None, es_computadora=False):
    color_fondo = colors.BLUE_GREY_100 if es_central else colors.WHITE
    color_borde = colors.BROWN if es_computadora else colors.BLACK
    
    # Usar representaciones pasadas o generar nuevas si no se proporcionaron
    repr1 = repr1 or obtener_representacion_valor(numero1)
    repr2 = repr2 or obtener_representacion_valor(numero2)
    
    # Determinar el tipo de cada representación
    tipo1, _ = repr1
    tipo2, _ = repr2
    
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(repr1),
                    alignment=ft.alignment.center,
                    # Solo usamos el color de fondo si es representación de números
                    bgcolor=color_fondo if tipo1 == "numero" else None,
                    width=60,
                    height=60,
                    # Solo añadimos borde si es representación de números
                    border=ft.border.all(1, color_borde) if tipo1 == "numero" else None
                ),
                ft.Container(
                    content=crear_contenido_ficha(repr2),
                    alignment=ft.alignment.center,
                    # Solo usamos el color de fondo si es representación de números
                    bgcolor=color_fondo if tipo2 == "numero" else None,
                    width=60,
                    height=60,
                    # Solo añadimos borde si es representación de números
                    border=ft.border.all(1, color_borde) if tipo2 == "numero" else None
                )
            ],
            spacing=1,
        ),
        bgcolor=color_borde,  # También cambiar el color del borde exterior
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
    
    # Determinar el tipo de cada representación
    tipo1, _ = repr1
    tipo2, _ = repr2
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=crear_contenido_ficha(repr1),
                    alignment=ft.alignment.center,
                    # Solo usamos el color de fondo si es representación de números
                    bgcolor=color_fondo if tipo1 == "numero" else None,
                    width=60,
                    height=60,
                    # Solo añadimos borde si es representación de números
                    border=ft.border.all(1, color_borde) if tipo1 == "numero" else None
                ),
                ft.Container(
                    content=crear_contenido_ficha(repr2),
                    alignment=ft.alignment.center,
                    # Solo usamos el color de fondo si es representación de números
                    bgcolor=color_fondo if tipo2 == "numero" else None,
                    width=60,
                    height=60,
                    # Solo añadimos borde si es representación de números
                    border=ft.border.all(1, color_borde) if tipo2 == "numero" else None
                )
            ],
            spacing=1,
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar los contenedores
        ),
        bgcolor=color_borde,  # También cambiar el color del borde exterior
        padding=1,
        border_radius=5,
        width=122  # Ancho fijo que corresponde a: 60 (ancho contenedor) * 2 + 1 (spacing) + 1 (padding izq/der)
    )

def crear_ficha_visual_jugador(ficha, on_drag_complete=None):
    """Crea una ficha visual arrastrable para el jugador con botón de rotación"""
    def crear_contenedor_numeros():
        # Determinar el tipo de cada representación
        tipo1, _ = ficha.repr1
        tipo2, _ = ficha.repr2
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=crear_contenido_ficha(ficha.repr1),
                        alignment=ft.alignment.center,
                        # Solo usamos el color de fondo si es representación de números
                        bgcolor=colors.WHITE if tipo1 == "numero" else None,
                        width=60,
                        height=60,
                        # Solo añadimos borde si es representación de números
                        border=ft.border.all(1, colors.BLACK) if tipo1 == "numero" else None
                    ),
                    ft.Container(
                        content=crear_contenido_ficha(ficha.repr2),
                        alignment=ft.alignment.center,
                        # Solo usamos el color de fondo si es representación de números
                        bgcolor=colors.WHITE if tipo2 == "numero" else None,
                        width=60,
                        height=60,
                        # Solo añadimos borde si es representación de números
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

def crear_zona_destino(page: ft.Page, estado_juego, posicion, on_ficha_jugada, area_juego, obtener_representacion_forzada=None):
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
            
            # Si tenemos la función obtener_representacion_forzada, la usamos para mantener consistencia visual
            if obtener_representacion_forzada:
                # Convertir representación para que coincida con el tablero central (es_para_jugador = False)
                repr1_central = obtener_representacion_forzada(ficha.numero1, False)
                repr2_central = obtener_representacion_forzada(ficha.numero2, False)
            else:
                # Si no tenemos la función, usamos la representación actual de la ficha
                repr1_central = ficha.repr1
                repr2_central = ficha.repr2
            
            # Crear nueva ficha visual según si es doble o no
            if (es_doble):
                ficha_visual = crear_ficha_visual_horizontal(ficha.numero1, ficha.numero2, repr1=repr1_central, repr2=repr2_central)
            else:
                ficha_visual = crear_ficha_visual(ficha.numero1, ficha.numero2, repr1=repr1_central, repr2=repr2_central)
            
            # Determinar índices y actualizar el área de juego
            if posicion == "arriba":
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[0]
                    # Reemplazar la zona actual con la ficha
                    area_juego.controls[indice_actual] = ficha_visual
                    # Crear nueva zona arriba
                    nueva_zona = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                    area_juego.controls.insert(0, nueva_zona)
            else:  # posicion == "abajo"
                indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                               if isinstance(control, ft.DragTarget)]
                if indices_zonas:
                    indice_actual = indices_zonas[-1]
                    # Reemplazar la zona actual con la ficha
                    area_juego.controls[indice_actual] = ficha_visual
                    # Crear nueva zona abajo
                    nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
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
    # TRUE: Tablero central con números y jugador con colores
    # FALSE: Tablero central con colores y jugador con números
    modo_central_numeros = random.choice([True, False])
    
    # Definir el mensaje según el modo
    modo_mensaje = ("El tablero central mostrará números y tus fichas colores" 
                   if modo_central_numeros else 
                   "El tablero central mostrará colores y tus fichas números")

    def obtener_representacion_forzada(numero, es_para_jugador):
        """Fuerza la representación según el modo de juego"""
        color, _ = COLORES_DOMINO[numero]
        if modo_central_numeros:
            # Centro usa números, jugador usa colores
            return ("numero", str(numero)) if not es_para_jugador else ("color", color)
        else:
            # Centro usa colores, jugador usa números
            return ("color", color) if not es_para_jugador else ("numero", str(numero))

    def convertir_fichas_segun_modo(fichas, es_para_jugador):
        """Convierte todas las fichas al modo correspondiente"""
        for ficha in fichas:
            ficha.repr1 = obtener_representacion_forzada(ficha.numero1, es_para_jugador)
            ficha.repr2 = obtener_representacion_forzada(ficha.numero2, es_para_jugador)
        return fichas

    def volver_al_menu_principal_click(e):
        volver_al_menu_principal(page)

    # Función para obtener el mensaje de la ficha inicial según el modo
    def get_mensaje_ficha_inicial(quien_empieza, ficha, usa_numeros_central):
        quien_txt = 'Tú empiezas' if quien_empieza == "jugador" else 'La computadora empieza'
        
        if usa_numeros_central:
            # Si el tablero central usa números, mostrar números
            return f"{quien_txt} con la ficha [{ficha.numero1}-{ficha.numero2}]"
        else:
            # Si el tablero central usa colores, mostrar nombres de colores
            _, nombre_color1 = COLORES_DOMINO[ficha.numero1]
            _, nombre_color2 = COLORES_DOMINO[ficha.numero2]
            return f"{quien_txt} con la ficha [{nombre_color1}-{nombre_color2}]"

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

    # Título de la página - reducido de tamaño
    titulo = ft.Text("Modo Principiante", size=24, color=colors.BLACK)
    volver_button = ft.ElevatedButton(
        text="Volver al menú",
        on_click=volver_al_menu_principal_click,
        width=120,  # Reducido de 200 a 120
        height=40   # Reducido de 50 a 40
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
    
    # Forzar la representación de la ficha central según el modo del tablero
    # Es importante que esto sea después de removerla y antes de crear el estado de juego
    ficha_central.repr1 = obtener_representacion_forzada(ficha_central.numero1, False)
    ficha_central.repr2 = obtener_representacion_forzada(ficha_central.numero2, False)
    
    estado_juego = EstadoJuego(ficha_central)

    def cerrar_dialogo(e):
        dlg.open = False
        page.update()

    # Mostrar mensaje del modo de juego más compacto con nombres de colores si corresponde
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

    def mostrar_mensaje(page, mensaje):
        """Muestra un mensaje temporal en la pantalla"""
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

    # Función para colocar una ficha especial en el tablero
    def colocar_ficha_especial(e=None):
        # Verificar los números actuales del tablero
        numero_arriba = estado_juego.numero_arriba
        numero_abajo = estado_juego.numero_abajo
        
        # Crear una ficha que coincida con alguno de los extremos
        # Generar un número aleatorio diferente al extremo con el que coincidirá
        if random.random() < 0.5:  # 50% probabilidad para elegir arriba o abajo
            # Crear ficha para arriba
            nuevo_numero = random.choice([n for n in range(10) if n != numero_arriba])
            ficha_especial = FichaDomino(999, nuevo_numero, numero_arriba)  # ID especial 999
            # Usar representación del tablero central (es_para_jugador = False)
            ficha_especial.repr1 = obtener_representacion_forzada(nuevo_numero, False)
            ficha_especial.repr2 = obtener_representacion_forzada(numero_arriba, False)
            lado_a_jugar = "arriba"
        else:
            # Crear ficha para abajo
            nuevo_numero = random.choice([n for n in range(10) if n != numero_abajo])
            ficha_especial = FichaDomino(999, numero_abajo, nuevo_numero)  # ID especial 999
            # Usar representación del tablero central (es_para_jugador = False)
            ficha_especial.repr1 = obtener_representacion_forzada(numero_abajo, False)
            ficha_especial.repr2 = obtener_representacion_forzada(nuevo_numero, False)
            lado_a_jugar = "abajo"
        
        # Añadir la ficha al área de juego
        if lado_a_jugar == "arriba":
            # Actualizar el número arriba
            estado_juego.numero_arriba = ficha_especial.numero1
            
            # Determinar si es una ficha doble
            es_doble = ficha_especial.numero1 == ficha_especial.numero2
            
            # Crear nueva ficha visual con borde café (es_computadora=True)
            ficha_visual = (
                crear_ficha_visual_horizontal(ficha_especial.numero1, ficha_especial.numero2, 
                                             repr1=ficha_especial.repr1, repr2=ficha_especial.repr2,
                                             es_computadora=True)
                if es_doble else
                crear_ficha_visual(ficha_especial.numero1, ficha_especial.numero2, 
                                  repr1=ficha_especial.repr1, repr2=ficha_especial.repr2,
                                  es_computadora=True)
            )
            
            # Encontrar la zona de arriba y reemplazarla
            indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                            if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[0]
                # Reemplazar la zona actual con la ficha
                area_juego.controls[indice_actual] = ficha_visual
                # Crear nueva zona arriba
                nueva_zona = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                area_juego.controls.insert(0, nueva_zona)
            
        else:  # lado_a_jugar == "abajo"
            # Actualizar el número abajo
            estado_juego.numero_abajo = ficha_especial.numero2
            
            # Determinar si es una ficha doble
            es_doble = ficha_especial.numero1 == ficha_especial.numero2
            
            # Crear nueva ficha visual con borde café (es_computadora=True)
            ficha_visual = (
                crear_ficha_visual_horizontal(ficha_especial.numero1, ficha_especial.numero2, 
                                             repr1=ficha_especial.repr1, repr2=ficha_especial.repr2,
                                             es_computadora=True)
                if es_doble else
                crear_ficha_visual(ficha_especial.numero1, ficha_especial.numero2, 
                                  repr1=ficha_especial.repr1, repr2=ficha_especial.repr2,
                                  es_computadora=True)
            )
            
            # Encontrar la zona de abajo y reemplazarla
            indices_zonas = [i for i, control in enumerate(area_juego.controls) 
                            if isinstance(control, ft.DragTarget)]
            if indices_zonas:
                indice_actual = indices_zonas[-1]
                # Reemplazar la zona actual con la ficha
                area_juego.controls[indice_actual] = ficha_visual
                # Crear nueva zona abajo
                nueva_zona = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
                area_juego.controls.append(nueva_zona)
        
        # Notificar al usuario con un mensaje más general
        mensaje = "La computadora ha jugado una ficha"
        mostrar_mensaje(page, mensaje)
        page.update()

    # Área de juego central scrolleable - altura reducida
    area_juego = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,  # Reducido de 10 a 5
        scroll=ft.ScrollMode.AUTO,  # Hacer scrolleable
        height=350,  # Reducido de 400 a 350
    )

    # Crear las zonas de destino y configurar área de juego inicial
    zona_arriba = crear_zona_destino(page, estado_juego, "arriba", on_ficha_jugada, area_juego, obtener_representacion_forzada)
    zona_abajo = crear_zona_destino(page, estado_juego, "abajo", on_ficha_jugada, area_juego, obtener_representacion_forzada)
    
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

    # Botón renombrado para hacer jugar al oponente - reducido
    boton_jugar_oponente = ft.ElevatedButton(
        text="Jugar oponente",  # Texto simplificado para que quepa en una línea
        tooltip="Hacer jugar al oponente",  # Tooltip con el texto completo
        on_click=colocar_ficha_especial,
        width=120,  # Mantenemos el ancho reducido
        height=40,  # Mantenemos la altura reducida
        style=ft.ButtonStyle(
            color=colors.WHITE,
            bgcolor=colors.BLUE_700
        )
    )

    # Modificar el contenedor principal
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                pozo_view,
                                volver_button  # Ya está debajo del pozo
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
                                    height=100,  # Altura fija reducida
                                ),
                                ft.Container(
                                    content=boton_jugar_oponente,  # Movido aquí, debajo de las cartas del oponente
                                    alignment=ft.alignment.center,
                                    padding=5,
                                ),
                                ft.Container(
                                    content=area_juego,
                                    height=350,  # Reducido para coincidir con area_juego
                                    border=ft.border.all(1, colors.GREY_400),
                                    border_radius=5,
                                    padding=5,  # Reducido de 10 a 5
                                ),
                                ft.Container(
                                    content=fichas_jugador_view,
                                    padding=2,
                                    height=150,  # Altura fija reducida
                                ),
                                # Se eliminó el contenedor del botón que estaba aquí
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

    page.update()





