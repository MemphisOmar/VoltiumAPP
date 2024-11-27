import flet as ft

def main(page: ft.Page):
    page.title = "VOLTIUM"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.background_color = ft.colors.LIME_ACCENT  # Cambia el color de fondo a azul claro

    def jugar_click(e):
        page.dialog = ft.AlertDialog(title=ft.Text("¡Comenzando el juego!"))
        page.dialog.open = True
        page.update()

    def ayuda_click(e):
        page.dialog = ft.AlertDialog(title=ft.Text("Ayuda del juego"))
        page.dialog.open = True
        page.update()

    def salir_click(e):
        page.window_close()

    jugar_button = ft.ElevatedButton(text="JUGAR", on_click=jugar_click, width=200, height=50)
    ayuda_button = ft.ElevatedButton(text="AYUDA", on_click=ayuda_click, width=200, height=50)
    salir_button = ft.ElevatedButton(text="SALIR", on_click=salir_click, width=200, height=50)

    page.add(
        ft.Column(
            [
                jugar_button,
                ayuda_button,
                salir_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)