import flet as ft
import os
import json

PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_profile.json")

class PerfilUsuarioForm(ft.Column):
    def __init__(self, on_submit):
        self.on_submit = on_submit
        text_style = ft.TextStyle(color="#222222", weight=ft.FontWeight.BOLD, size=22)
        self.id_input = ft.TextField(label="ID", width=260, bgcolor="#FFFFFF", color="#222222", text_style=text_style, border_color="#222222", border_width=3, border_radius=10)
        self.edad_input = ft.TextField(label="Edad", width=260, keyboard_type=ft.KeyboardType.NUMBER, bgcolor="#FFFFFF", color="#222222", text_style=text_style, border_color="#222222", border_width=3, border_radius=10)
        self.sexo_input = ft.Dropdown(label="Sexo", width=260, options=[ft.dropdown.Option("M"), ft.dropdown.Option("F"), ft.dropdown.Option("Otro")], bgcolor="#FFFFFF", color="#222222", text_style=text_style, border_color="#222222", border_width=3, border_radius=10)
        self.carrera_input = ft.TextField(label="Carrera", width=260, bgcolor="#FFFFFF", color="#222222", text_style=text_style, border_color="#222222", border_width=3, border_radius=10)
        self.grupo_input = ft.TextField(label="Grupo", width=260, bgcolor="#FFFFFF", color="#222222", text_style=text_style, border_color="#222222", border_width=3, border_radius=10)
        self.submit_btn = ft.ElevatedButton(text="Guardar Perfil", on_click=self.submit, bgcolor="#222222", color="#FFFFFF", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=ft.padding.symmetric(horizontal=18, vertical=10), text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=18)))
        super().__init__(
            controls=[
                ft.Container(
                    content=ft.Column([
                        self.id_input,
                        self.edad_input,
                        self.sexo_input,
                        self.carrera_input,
                        self.grupo_input,
                        self.submit_btn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#FFFFFF",
                    border_radius=20,
                    padding=36,
                    shadow=ft.BoxShadow(blur_radius=18, color="#0000001A"),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def submit(self, e):
        perfil = {
            "id": self.id_input.value,
            "edad": self.edad_input.value,
            "sexo": self.sexo_input.value,
            "carrera": self.carrera_input.value,
            "grupo": self.grupo_input.value
        }
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(perfil, f)
        self.on_submit(perfil)

def mostrar_formulario_perfil(page, on_perfil_guardado):
    page.clean()
    page.add(
        ft.Container(
            content=PerfilUsuarioForm(on_perfil_guardado),
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()
