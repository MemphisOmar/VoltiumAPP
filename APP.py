import flet as ft

def main(page: ft.Page):
    page.title = "Menú del Videojuego"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def jugar_click(e):
        page.dialog = ft.AlertDialog(title=ft.Text("¡Comenzando el juego!"))
        page.dialog.open = True
        page.update()

    def ayuda_click(e):
        page.dialog = ft.AlertDialog(title=ft.Text("Ayuda del juego"))
        page.dialog.open = True
        page.update()

    jugar_button = ft.ElevatedButton(text="JUGAR", on_click=jugar_click)
    ayuda_button = ft.ElevatedButton(text="AYUDA", on_click=ayuda_click)

    page.add(
        ft.Column(
            [
                jugar_button,
                ayuda_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)