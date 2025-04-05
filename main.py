import flet as ft
from views import principal

def main(page: ft.Page):

    def cam_ventana(route):
        page.controls.clear()
        if page.route == "/principal_menu":
            principal.principal(page)
        else:
            page.add(ft.Text("Ruta no encontrada"))

    page.on_route_change = cam_ventana
    page.go(page.route)

    page.window.width = 450
    page.window.height = 600
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.title = "StormCargoGest"

    page.add(
        ft.Container(
            ft.Column([
                # Titulo
                ft.Container(
                    ft.Text("Iniciar Sesión", width=380, size=30, text_align="center", weight="w900"),
                    ft.padding.only(10, 100, 0, 20)
                ),
                # TextField del Usuario
                ft.Container(
                    ft.TextField(width=350, hint_text="Ingrese su Usuario", color="white", prefix_icon= ft.icons.PERSON),
                    ft.padding.only(20),
                ),
                # TextField de la Contraseña
                ft.Container(
                    ft.TextField(width=350, hint_text="Ingrese su Contraseña", color="white", prefix_icon= ft.icons.LOCK, password=True, can_reveal_password=True),
                    ft.padding.only(20),
                ),
                # Button para Iniciar Sesion
                ft.Container(
                    ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=lambda e: page.go("/principal_menu")),
                    ft.padding.only(60, 30),
                ),

                ft.Container(
                    ft.TextButton(text="Crear Usuario"),
                    ft.padding.only(150)
                )
            ]
            ),
            border_radius=20,
            width=400,
            height=530,
            bgcolor="#673AB7"
        )
    )

ft.app(target=main)