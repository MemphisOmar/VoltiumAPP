import flet as ft
import webbrowser

def mostrar_ayuda(page: ft.Page):
    def cerrar_ayuda(e=None):
        if overlay_ayuda in page.overlay:
            page.overlay.remove(overlay_ayuda)
            page.update()

    def mostrar_codigo_colores(e):
        contenido_ayuda.content = ft.Column([
            ft.Image(src="MAIN/Resistencia.png", width=320, height=320, fit=ft.ImageFit.CONTAIN),
            ft.ElevatedButton("Regresar", on_click=mostrar_menu_ayuda)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    def abrir_explicacion(e):
        webbrowser.open("https://www.youtube.com/shorts/nbPFl_Icn78")
        
    def mostrar_menu_ayuda(e=None):
        contenido_ayuda.content = ft.Column([
            ft.Text("¿Qué tipo de ayuda necesita?", size=20, weight=ft.FontWeight.BOLD, color="black"),
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
                "Cerrar Ayuda",
                on_click=cerrar_ayuda,
                width=200,
                height=50,
                color="white",
                bgcolor="#29c589"
            )
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    contenido_ayuda = ft.Container(
        content=None,
        padding=30,
        width=380,
        height=420,
        bgcolor="#29c589",  # Verde sólido igual al menú principal
        border_radius=30,
        alignment=ft.alignment.center
    )

    overlay_ayuda = ft.Container(
        content=ft.Column([
            ft.Container(
                content=contenido_ayuda,
                alignment=ft.alignment.center,
                bgcolor=None,
                border_radius=30,
                padding=0,
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#00000033",  # Fondo overlay muy transparente
        alignment=ft.alignment.center,
        expand=True
    )

    page.overlay.append(overlay_ayuda)
    mostrar_menu_ayuda()
    page.update()