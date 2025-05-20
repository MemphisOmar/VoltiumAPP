import flet as ft
from flet import colors
from juegoPrincipiante import configurar_ventana_domino #Importar la subrutina desde juego.py
import random
from db_manager import DBManager
import time

def configurar_ventana_juego(page: ft.Page, volver_al_menu_principal):
    def volver_al_menu_principal_click(e):
        volver_al_menu_principal(page)
    
    def modo_principiante_click(e):
        configurar_ventana_domino(page, volver_al_menu_principal)
 
    def modo_facil_click(e):
        configurar_ventana_facil(page, configurar_ventana_juego, volver_al_menu_principal)

    def modo_medio_click(e):
        configurar_ventana_medio(page, configurar_ventana_juego, volver_al_menu_principal)

    def modo_dificil_click(e):
        configurar_ventana_dificil(page, configurar_ventana_juego, volver_al_menu_principal)

    page.clean()  # Limpiar la página actual
    page.title="Juego - VOLTIUM"
    page.bgcolor="#fff1b9"
    page.window_width=720
    page.window_height=1280
    page.window_resizable=False
    page.padding=0
    page.margin=0


    game_title=ft.Text("Selecciona el modo de juego", size=30, color=colors.BLACK)
    volver_button=ft.ElevatedButton(text="Volver al menú principal", on_click=volver_al_menu_principal_click, width=200, height=50)
    principiante_button=ft.ElevatedButton(text="Modo Principiante", on_click=modo_principiante_click, width=200, height=50)
    facil_button=ft.ElevatedButton(text="Modo de Juego Fácil", on_click=modo_facil_click, width=200, height=50)
    medio_button=ft.ElevatedButton(text="Modo de Juego Medio", on_click=modo_medio_click, width=200, height=50)
    dificil_button=ft.ElevatedButton(text="Modo de Juego Difícil", on_click=modo_dificil_click, width=200, height=50)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    game_title,
                    principiante_button,
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



def obtener_codigo_colores(resistencia):
    colores = {
        0: colors.BLACK,    # Negro
        1: colors.BROWN,    # Marrón
        2: colors.RED,      # Rojo
        3: colors.ORANGE,   # Naranja
        4: colors.YELLOW,   # Amarillo
        5: colors.GREEN,    # Verde
        6: colors.BLUE,     # Azul
        7: colors.PURPLE,   # Violeta
        8: colors.GREY,     # Gris
        9: colors.WHITE     # Blanco
    }
    
    resistencia_str = str(resistencia)
    
    if len(resistencia_str) <= 3:
        primera_banda = int(resistencia_str[0]) if len(resistencia_str) >= 1 else 0
        segunda_banda = int(resistencia_str[1]) if len(resistencia_str) >= 2 else 0
        multiplicador = len(resistencia_str) - 2 if len(resistencia_str) > 2 else 0
        
        return [
            colores[primera_banda],   # Color para primera banda
            colores[segunda_banda],   # Color para segunda banda
            colores[multiplicador]    # Color para multiplicador
        ]
    
    else:
        primera_banda = int(resistencia_str[0])
        segunda_banda = int(resistencia_str[1])
        multiplicador = len(resistencia_str) - 3
        
        return [
            colores[primera_banda],   # Color para primera banda
            colores[segunda_banda],   # Color para segunda banda
            colores[multiplicador]    # Color para multiplicador
        ]

def configurar_ventana_facil(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    db = DBManager()
    tiempo_inicio = time.time()  # Iniciamos el tiempo inmediatamente
    tiempo_total = 0
    puntaje = 100  # Puntaje inicial
    timer_active = True
    
    def update_cronometro(e):
        if not timer_active or not tiempo_inicio:
            return
        
        tiempo_actual = time.time()
        tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60
        texto_cronometro.value = f"Tiempo: {minutos:02d}:{segundos:02d}"
        page.update()
        
        if timer_active:
            page.invoke_after(1, update_cronometro)

    def mostrar_dialogo_registro(puntaje_final, tiempo_total):
        nombre_input = ft.TextField(label="Nombre", width=300)
        grupo_input = ft.TextField(label="Grupo", width=300)
        
        def guardar_registro(e):
            nombre = nombre_input.value
            grupo = grupo_input.value
            
            if nombre and grupo:
                # Guardar en la base de datos
                db.actualizar_puntaje(nombre, grupo, puntaje_final, tiempo_total)
                dlg.open = False
                page.update()
                # Volver al menú de juego
                volver_al_menu_juego(page, volver_al_menu_principal)
            else:
                error_dlg = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("Por favor, completa todos los campos"),
                )
                page.dialog = error_dlg
                error_dlg.open = True
                page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("¡Juego Terminado!"),
            content=ft.Column([
                ft.Text(f"Tiempo total: {tiempo_total//60:02d}:{tiempo_total%60:02d}"),
                ft.Text(f"Puntaje final: {puntaje_final}"),
                ft.Text("Ingresa tus datos para guardar tu puntuación:"),
                nombre_input,
                grupo_input,
            ], tight=True),
            actions=[
                ft.ElevatedButton("Guardar", on_click=guardar_registro)
            ],
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()

    def finalizar_juego():
        nonlocal tiempo_total, puntaje, timer_active
        timer_active = False
        tiempo_total = int(time.time() - tiempo_inicio)
        # Calcular puntaje final basado en el tiempo y los intentos
        puntaje_final = max(0, puntaje - (tiempo_total // 30))  # Reducir puntos cada 30 segundos
        mostrar_dialogo_registro(puntaje_final, tiempo_total)

    # Crear el texto del cronómetro antes de usarlo
    texto_cronometro = ft.Text("Tiempo: 00:00", size=20, color=colors.BLACK)

    def volver_al_menu_click(e):
        page.clean()
        volver_al_menu_juego(page, volver_al_menu_principal)

    # Añadir el texto del cronómetro a la interfaz
    texto_cronometro = ft.Text("Tiempo: 00:00", size=20, color=colors.BLACK)

    intentos = 0  # Add counter at start
    # Configuración inicial de la ventana
    page.clean()
    page.title = "Modo de Juego Fácil"
    page.bgcolor = colors.WHITE
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False

    # Selección de resistencia aleatoria y generación de código de colores
    resistencias_comerciales = [10, 22, 330, 100, 220, 470, 1000, 2200, 4700, 10_000]
    numero_random = random.choice(resistencias_comerciales)
    codigo_colores = obtener_codigo_colores(numero_random)

    # Crear una lista con todos los colores posibles
    todos_los_colores = [colors.BLACK, colors.BROWN, colors.RED, colors.ORANGE, 
                        colors.YELLOW, colors.GREEN, colors.BLUE, colors.PURPLE, 
                        colors.GREY, colors.WHITE]
    
    # Asegurarse de que los colores correctos estén incluidos
    colores_juego = codigo_colores.copy()
    
    # Remover los colores correctos de la lista de todos los colores
    for color in colores_juego:
        if color in todos_los_colores:
            todos_los_colores.remove(color)
    
    # Seleccionar aleatoriamente los colores adicionales para completar las opciones
    colores_adicionales = random.sample(todos_los_colores, 7)  # 7 + 3 = 10 colores en total
    
    # Combinar y mezclar todos los colores para las opciones
    colores_opciones = colores_juego + colores_adicionales
    random.shuffle(colores_opciones)

    # Modificar la función crear_receptor_color para usar los colores mezclados
    def crear_receptor_color(color):
        return ft.Draggable(
            content=ft.Container(
                width=100,
                height=100,
                bgcolor=color,
                border_radius=ft.border_radius.all(10),
                padding=ft.padding.all(10)
            )
        )

    # Crear los receptores con los colores mezclados
    receptores = [crear_receptor_color(color) for color in colores_opciones[:10]]  # Limitamos a 10 opciones
    
    # Crear la fila de receptores con los nuevos colores mezclados
    receptores_row = ft.Row(
        controls=receptores,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        wrap=True  # Permite que los receptores se envuelvan en múltiples filas si no caben
    )

    def verificar_respuesta(e=None):
        nonlocal intentos, puntaje
        color1 = drop_target1.content.bgcolor
        color2 = drop_target2.content.bgcolor
        color3 = drop_target3.content.bgcolor
        
        # Obtener los valores numéricos según el código de colores
        def obtener_valor_color(color):
            colores_valores = {
                colors.BLACK: 0,    # Negro
                colors.BROWN: 1,    # Marrón
                colors.RED: 2,      # Rojo
                colors.ORANGE: 3,   # Naranja
                colors.YELLOW: 4,   # Amarillo
                colors.GREEN: 5,    # Verde
                colors.BLUE: 6,     # Azul
                colors.PURPLE: 7,   # Violeta
                colors.GREY: 8,     # Gris
                colors.WHITE: 9     # Blanco 
            }
            return colores_valores.get(color)

        # Obtener valores numéricos de los colores seleccionados
        valor1 = obtener_valor_color(color1)
        valor2 = obtener_valor_color(color2)
        multiplicador = obtener_valor_color(color3)

        # Calcular el valor de la resistencia según los colores seleccionados
        if valor1 is not None and valor2 is not None and multiplicador is not None:
            valor_seleccionado = (valor1 * 10 + valor2) * (10 ** multiplicador)
            
            if valor_seleccionado == numero_random:
                puntaje += 50  # Bonus por respuesta correcta
                dlg = ft.AlertDialog(
                    title=ft.Text("¡Correcto!"),
                    content=ft.Text(f"¡Has acertado! El valor {numero_random}Ω corresponde a los colores seleccionados.")
                )
                page.dialog = dlg
                dlg.open = True
                finalizar_juego()
            else:
                intentos += 1
                puntaje -= 25  # Penalización por respuesta incorrecta
                if intentos >= 2:
                    dlg = ft.AlertDialog(
                        title=ft.Text("Límite de intentos alcanzado"),
                        content=ft.Text(f"La respuesta correcta era {numero_random}Ω.")
                    )
                    page.dialog = dlg
                    dlg.open = True
                    finalizar_juego()
                else:
                    dlg = ft.AlertDialog(
                        title=ft.Text("Incorrecto"),
                        content=ft.Text(f"El valor {valor_seleccionado}Ω no es correcto. Te queda {2-intentos} intento.")
                    )
                    page.dialog = dlg
                    dlg.open = True
        
        page.update()

    # Crear las zonas donde se soltarán los colores
    def on_accept(e):
        src = page.get_control(e.src_id)
        if src:
            e.control.content.bgcolor = src.content.bgcolor
            page.update()

    def crear_drop_target():
        return ft.DragTarget(
            content=ft.Container(
                width=100,
                height=100,
                bgcolor=colors.GREY_200,
                border_radius=ft.border_radius.all(10),
                padding=ft.padding.all(10)
            ),
            on_accept=on_accept
        )

    # Crear los receptores y zonas de destino
    receptor1 = crear_receptor_color(codigo_colores[0])
    receptor2 = crear_receptor_color(codigo_colores[1])
    receptor3 = crear_receptor_color(codigo_colores[2])

    drop_target1 = crear_drop_target()
    drop_target2 = crear_drop_target()
    drop_target3 = crear_drop_target()

    # Crear filas de receptores y destinos
    drop_targets_row = ft.Row(
        controls=[drop_target1, drop_target2, drop_target3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Botón de verificación
    boton_verificar = ft.ElevatedButton(
        text="Verificar respuesta",
        on_click=verificar_respuesta
    )

    # Botón para volver al menú
    boton_volver = ft.ElevatedButton(
        text="Volver al menú",
        on_click=volver_al_menu_click
    )

    def reset_targets(e):
        drop_target1.content.bgcolor = colors.GREY_200
        drop_target2.content.bgcolor = colors.GREY_200
        drop_target3.content.bgcolor = colors.GREY_200
        page.update()

    # Botón de reinicio
    boton_reiniciar = ft.ElevatedButton(
        text="Reiniciar",
        on_click=reset_targets
    ) 

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    texto_cronometro,  # Añadir el cronómetro
                     ft.Image(
                        src="MAIN/resistor_facil.png",
                        width=400,
                        height=200,
                        fit=ft.ImageFit.CONTAIN
                     ),
                    ft.Text(f"Resistencia: {numero_random} Ω", size=30),
                    receptores_row,
                    ft.Container(height=20),
                    drop_targets_row,
                    ft.Container(height=20),
                    ft.Row(
                        controls=[boton_verificar, boton_reiniciar, boton_volver],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.alignment.top_center,
            padding=20
        )
    )
    
    page.update()
    update_cronometro(None)  # Start the timer

def configurar_ventana_medio(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    numero_random=random.randrange(100, 10001, 10)


    page.clean()
    page.title = "Modo de Juego Medio"
    page.bgcolor = colors.WHITE
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.margin = 0

    medio_title = ft.Text("Modo de Juego Medio", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(
        text="Volver al menú de modos",
        on_click=volver_al_menu_click,
        width=200,
        height=50
    )

    #Contenedores
    receptor1 = ft.Container(
        content=ft.Text("Receptor 1"),
        width=100,
        height=100,
        bgcolor=colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),  
        padding=ft.padding.all(10)  
    )

    receptor2 = ft.Container(
        content=ft.Text("Receptor 2"),
        width=100,
        height=100,
        bgcolor=colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10), 
        padding=ft.padding.all(10)  
    )

    receptor3 = ft.Container(
        content=ft.Text("Receptor 3"),
        width=100,
        height=100,
        bgcolor=colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),  
        padding=ft.padding.all(10)  
    )

    #FIla de receptores
    receptores_row = ft.Row(
        controls=[receptor1, receptor2, receptor3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

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
                    ft.Image(src="MAIN/resistor_medio.png"),
                    ft.Container( 
                        content=ft.Text(str(numero_random), size=24, color=colors.BLACK), 
                        alignment=ft.alignment.center, 
                        bgcolor=colors.GREY_200, 
                        padding=ft.padding.all(10), 
                        border_radius=ft.border_radius.all(10), 
                    )
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

    

    #Layout
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    receptores_row  
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            ),
            expand=True
        )
    )

    page.update()

def configurar_ventana_dificil(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    numero_random=random.randrange(100, 10001, 10)

    page.clean()
    page.title = "Modo de Juego Dificil"
    page.bgcolor = colors.WHITE
    page.window_width = 720
    page.window_height=1280
    page.window_resizable = False
    page.padding = 0
    page.margin = 0

    dificil_title = ft.Text("Modo de Juego Dificil", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(
        text="Volver al menú de modos",
        on_click=volver_al_menu_click,
        width=200,
        height=50
    )

    #Contenedores
    receptor1 = ft.Container(
        content=ft.Text("Receptor 1"),
        width=100,
        height=100,
        bgcolor=colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),  
        padding=ft.padding.all(10)  
    )

    receptor2 = ft.Container(
        content=ft.Text("Receptor 2"),
        width=100,
        height=100,
        bgcolor=colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10), 
        padding=ft.padding.all(10)  
    )

    receptor3 = ft.Container(
        content=ft.Text("Receptor 3"),
        width=100,
        height=100,
        bgcolor=colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),  
        padding=ft.padding.all(10)  
    )

    #FIla de receptores
    receptores_row = ft.Row(
        controls=[receptor1, receptor2, receptor3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

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
                    ft.Image(src="MAIN/resistor_dificil.png"),
                    ft.Container( 
                        content=ft.Text(str(numero_random), size=24, color=colors.BLACK), 
                        alignment=ft.alignment.center, 
                        bgcolor=colors.GREY_200, 
                        padding=ft.padding.all(10), 
                        border_radius=ft.border_radius.all(10), 
                    )
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

    

    #Layout
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    receptores_row  
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            ),
            expand=True
        )
    )

    page.update()

