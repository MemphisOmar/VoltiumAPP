import flet as ft
import random

class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0
        self.slot_occupied = False
        self.current_slot_top = 110

def main(page: ft.Page):
    page.bgcolor = ft.colors.WHITE

    # Global declarations
    global main_color_index
    global draggable_dominos
    global placed_dominos

    # Initialize globals
    main_color_index = random.randint(0, 9)
    draggable_dominos = []
    placed_dominos = []



    page.window_width = 720
    page.window_height = 1280
    
    colores = {
        0: ft.colors.BLACK,
        1: ft.colors.BROWN,
        2: ft.colors.RED,
        3: ft.colors.ORANGE,
        4: ft.colors.YELLOW,
        5: ft.colors.GREEN,
        6: ft.colors.BLUE,
        7: ft.colors.PURPLE,
        8: ft.colors.GREY,
        9: ft.colors.WHITE
    }

    def generate_new_game_state():
        new_color_index = random.randint(0, 9)
        # Solo incluir el número que coincide con el nuevo color principal
        new_numbers = [new_color_index]
        for _ in range(2):
            new_numbers.append(random.randint(0, 9))
        random.shuffle(new_numbers)
        
        new_dominos = []
        for i in range(3):
            random_color = colores[random.randint(0, 9)]
            new_domino = ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=5,
                on_pan_start=start_drag,
                on_pan_update=drag,
                on_pan_end=drop,
                left=50 + i * 100,
                top=400,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(str(new_numbers[i]), size=20, color=ft.colors.BLACK),
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.WHITE,
                            border=ft.border.all(1, ft.colors.BLACK)
                        ),
                        ft.Container(
                            width=50,
                            height=50,
                            bgcolor=random_color,
                            border=ft.border.all(1, ft.colors.BLACK)
                        )
                    ],
                    spacing=0
                )
            )
            new_dominos.append(new_domino)
        return new_dominos, new_color_index

    def add_new_slot():
        solitaire.current_slot_top += 110
        new_slot = ft.Container(
            width=50,
            height=100,
            top=solitaire.current_slot_top,
            left=200,
            border=ft.border.all(1, ft.colors.BLACK)
        )
        return new_slot

    def place(card, slot):
        global main_color_index, draggable_dominos, placed_dominos
        dragged_number = int(card.content.controls[0].content.value)
        if not solitaire.slot_occupied and dragged_number == main_color_index:
            card.top = slot.top
            card.left = slot.left
            solitaire.slot_occupied = True
            
            # Add current domino to placed list
            placed_dominos.append(card)

            # Remove only unplaced draggable dominos
            for domino in draggable_dominos:
                if domino not in placed_dominos:
                    page.controls[0].controls.remove(domino)

            # Add new slot
            new_slot = add_new_slot()
            page.controls[0].controls.append(new_slot)

            # Generate and add new dominos
            new_dominos, new_main_color_index = generate_new_game_state()
            main_color_index = new_main_color_index
            page.controls[0].controls.extend(new_dominos)
            draggable_dominos = new_dominos
            
            solitaire.slot_occupied = False
            page.update()
        else:
            bounce_back(solitaire, card)

    def bounce_back(game, card):
        card.top = game.start_top
        card.left = game.start_left

    def start_drag(e: ft.DragStartEvent):
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()
    
    def drop(e: ft.DragEndEvent):
        if (
            abs(e.control.top - slot.top) < 20
            and abs(e.control.left - slot.left) < 20
        ):
            place(e.control, slot)
        else:
            bounce_back(solitaire, e.control)
        e.control.update()

    # Main domino at top
    main_domino = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(str(random.randint(0, 9)), size=20, color=ft.colors.BLACK),
                width=50,
                height=50,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.BLACK)
            ),
            ft.Container(
                width=50,
                height=50,
                bgcolor=colores[main_color_index],
                border=ft.border.all(1, ft.colors.BLACK)
            )
        ],
        spacing=0,
        top=0,
        left=200
    )

    # Initial slot
    slot = ft.Container(
        width=50,
        height=100,
        top=110,
        left=200,
        border=ft.border.all(1, ft.colors.BLACK)
    )

    # Initial draggable dominos
    numbers = [main_color_index]
    for _ in range(2):
        numbers.append(random.randint(0, 9))
    random.shuffle(numbers)

    for i in range(3):
        random_color = colores[random.randint(0, 9)]
        domino = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            left=50 + i * 100,
            top=400,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(str(numbers[i]), size=20, color=ft.colors.BLACK),
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.BLACK)
                    ),
                    ft.Container(
                        width=50,
                        height=50,
                        bgcolor=random_color,
                        border=ft.border.all(1, ft.colors.BLACK)
                    )
                ],
                spacing=0
            )
        )
        draggable_dominos.append(domino)

    solitaire = Solitaire()

    page.add(
        ft.Stack(
            controls=[main_domino, slot] + draggable_dominos,
            width=1000,
            height=500
        )
    )

ft.app(target=main)