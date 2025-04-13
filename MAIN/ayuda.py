import flet as ft
import webbrowser

def mostrar_ayuda(page: ft.Page):
    def regresar_menu(e):
        dlg.open = False
        page.update()
        from MAIN.APP import main
        main(page)

    def mostrar_codigo_colores(e):
        contenido_ayuda.content = ft.Column([
            ft.Image(src="MAIN/Resistencia.png", width=400, height=400, fit=ft.ImageFit.CONTAIN),
            ft.ElevatedButton("Regresar", on_click=lambda e: mostrar_menu_ayuda(e))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    def abrir_explicacion(e):
        webbrowser.open("https://www.youtube.com/shorts/nbPFl_Icn78")
        
    def mostrar_menu_ayuda(e):
        contenido_ayuda.content = ft.Column([
            ft.Text("¿Qué tipo de ayuda necesita?", size=20, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Código de Colores",
                on_click=mostrar_codigo_colores,
                width=200,
                height=50,
                color="white",
                bgcolor="#29c589"
            ),
            ft.ElevatedButton(
                "Video Explicativo",
                on_click=abrir_explicacion,
                width=200,
                height=50,
                color="white",
                bgcolor="#29c589"
            ),
            ft.ElevatedButton(
                "Regresar al Menú",
                on_click=regresar_menu,
                width=200,
                height=50,
                color="white",
                bgcolor="#29c589"
            )
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    contenido_ayuda = ft.Container(
        content=None,
        padding=20,
        width=500,
        bgcolor="#88B98A",
        border_radius=10
    )

    dlg = ft.AlertDialog(
        content=contenido_ayuda,
        modal=True
    )

    page.dialog = dlg
    dlg.open = True
    mostrar_menu_ayuda(None)
    page.update()