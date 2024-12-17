import flet as ft
from flet import colors
import random

def configurar_ventana_juego(page: ft.Page, volver_al_menu_principal):
    def volver_al_menu_principal_click(e):
        volver_al_menu_principal(page)
    
    def modo_principiante_click(e):
        configurar_ventana_principiante(page, configurar_ventana_juego, volver_al_menu_principal)

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

def configurar_ventana_principiante(page: ft.Page, volver_al_menu_juego, volver_al_menu_principal):
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    numero_random = random.randrange(100, 10001, 10)

    page.clean()
    page.title = "Modo de Juego Principiante"
    page.bgcolor = colors.WHITE
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.margin = 0

    principiante_title = ft.Text("Modo Principiante", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(
        text="Volver al menú de modos",
        on_click=volver_al_menu_click,
        width=200,
        height=50
    )

    # Diccionario de colores con números asignados
    colores = {
        0: colors.BLACK,
        1: colors.BROWN,
        2: colors.RED,
        3: colors.ORANGE,
        4: colors.YELLOW,
        5: colors.GREEN,
        6: colors.BLUE,
        7: colors.PURPLE,
        8: colors.GREY,
        9: colors.WHITE
    }

    # Seleccionar un color aleatorio
    numero_color_aleatorio = random.choice(list(colores.keys()))
    color_aleatorio = colores[numero_color_aleatorio]

    # Pieza de dominó principal
    domino_piece = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    bgcolor=colors.WHITE,
                    width=50,
                    height=50,
                    border=ft.border.all(1, colors.BLACK)  # Borde negro alrededor del recuadro de color
                ),
                ft.Container(
                    bgcolor=color_aleatorio,
                    width=50,
                    height=50,
                    border=ft.border.all(1, colors.BLACK)  # Borde negro alrededor del recuadro blanco
                )
            ],
            spacing=0
        ),
        alignment=ft.alignment.center,
        width=50,
        height=100,
        border=ft.border.all(1, colors.BLACK)  # Borde negro alrededor de toda la pieza de dominó
    )

    # Función para crear una pieza de dominó adicional
    def crear_domino():
        numero_color_aleatorio = random.choice(list(colores.keys()))
        color_aleatorio = colores[numero_color_aleatorio]
        numero_aleatorio = random.randint(0, 9)
        return ft.Draggable(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(str(numero_aleatorio), size=20, color=colors.BLACK),
                            bgcolor=colors.WHITE,
                            width=50,
                            height=50,
                            border=ft.border.all(1, colors.BLACK)  # Borde negro alrededor del recuadro de color
                        ),
                        ft.Container(
                            bgcolor=color_aleatorio,
                            width=50,
                            height=50,
                            border=ft.border.all(1, colors.BLACK)  # Borde negro alrededor del recuadro blanco
                        )
                    ],
                    spacing=0
                ),
                alignment=ft.alignment.center,
                width=50,
                height=100,
                border=ft.border.all(1, colors.BLACK)  # Borde negro alrededor de toda la pieza de dominó
            ),
            data=f"{numero_aleatorio}-{list(colores.keys())[list(colores.values()).index(color_aleatorio)]}"  # Añadir datos para identificar el dominó
        )

    # Crear 3 piezas de dominó adicionales
    dominos_adicionales = [crear_domino() for _ in range(3)]

    # Contenedor para arrastrar y soltar
    def on_accept(e):
        # Obtener los datos del dominó arrastrado
        data = e.data
        if '-' in data:
            numero, color = data.split('-')
            color = int(color)
            color_aleatorio = colores[color]
            
            # Actualizar el contenido del DragTarget con el dominó arrastrado
            e.control.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(numero, size=20, color=colors.BLACK),
                            bgcolor=colors.WHITE,
                            width=50,
                            height=50,
                            border=ft.border.all(1, colors.BLACK)
                        ),
                        ft.Container(
                            bgcolor=color_aleatorio,
                            width=50,
                            height=50,
                            border=ft.border.all(1, colors.BLACK)
                        )
                    ],
                    spacing=0
                ),
                alignment=ft.alignment.center,
                width=50,
                height=100,
                border=ft.border.all(1, colors.BLACK)
            )
            page.update()

    drag_target = ft.DragTarget(
        content=ft.Container(
            width=50,
            height=100,
            border=ft.border.all(1, colors.BLACK),
            alignment=ft.alignment.center
        ),
        on_accept=on_accept
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    principiante_title,
                    ft.Container(
                        content=volver_button,
                        alignment=ft.alignment.top_right
                    ),
                    domino_piece,  # Añadir la pieza de dominó
                    drag_target  # Añadir el contenedor para arrastrar y soltar
                ],
                alignment=ft.MainAxisAlignment.START,
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
                    ft.Row(dominos_adicionales, alignment=ft.MainAxisAlignment.CENTER)  # Añadir las piezas de dominó adicionales
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.alignment.top_center,
            width=1024,
            height=768,
            padding=ft.padding.only(bottom=100)  # Ajusta el margen inferior según sea necesario
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
    def volver_al_menu_click(e):
        volver_al_menu_juego(page, volver_al_menu_principal)

    resistencias_comerciales = [10, 22, 330, 100, 220, 470, 1000, 2200, 4700, 10_000]


    numero_random=random.choice(resistencias_comerciales)

    codigo_colores = obtener_codigo_colores(numero_random)

    page.clean()
    page.title = "Modo de Juego Facil"
    page.bgcolor = colors.WHITE
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.margin = 0

    facil_title = ft.Text("Modo de Juego Facil", size=30, color=colors.BLACK)
    volver_button = ft.ElevatedButton(
        text="Volver al menú de modos",
        on_click=volver_al_menu_click,
        width=200,
        height=50
    )


    receptor1 = ft.Container(
        width=100,
        height=100,
        bgcolor=codigo_colores[0],  # Primer color
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),  
        padding=ft.padding.all(10)  
    )

    receptor2 = ft.Container(
        width=100,
        height=100,
        bgcolor=codigo_colores[1],  # Segundo color
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10), 
        padding=ft.padding.all(10)  
    )

    receptor3 = ft.Container(
        width=100,
        height=100,
        bgcolor=codigo_colores[2],  # Color del multiplicador
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
                    ft.Image(src="resistor_facil.png"),
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
                    ft.Image(src="resistor_medio.png"),
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
    page.window_height = 1280
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
                    ft.Image(src="resistor_dificil.png"),
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