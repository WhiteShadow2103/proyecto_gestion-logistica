import flet as ft

def main(page: ft.Page):
   
    def route_change(route):
        page.views.clear()
        page.window.width = 420
        page.window.height = 590
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.title = "StormCargoGest"
        page.views.append(
            ft.View(
                "/",
                [
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
                            ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=lambda e: page.go("/principal")),
                            ft.padding.only(60, 30),
                        ),
                        # Button para Crear Usuario
                        ft.Container(
                             ft.TextButton(text="Crear Usuario"),
                            ft.padding.only(150)
                        )
                    ]
                    ),
                        border_radius=8,
                        width=400,
                        height=530,
                        bgcolor="#673AB7"
                    ),
                ],
            )
        )
        if page.route == "/principal":
            page.window.width = 1200
            page.window.height = 800
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.views.append(
                ft.View(
                    "/principal",
                    [   
                        ft.Container(
                            ft.Column([
                                ft.Container(
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Text("Salir"),
                                                margin=10,
                                                padding=10,
                                                alignment=ft.alignment.center,
                                                bgcolor=ft.Colors.RED,
                                                width=65,
                                                height=40,
                                                border_radius=10,
                                                ink=True,
                                                on_click=lambda _: page.go("/"), 
                                            ),
                                            ft.Container(
                                                content=ft.Text("Gestión Interna", weight="w900", size=18),
                                                margin=1,
                                                padding=1,
                                                alignment=ft.alignment.center_left,
                                                width=350,
                                                height=40
                                            )
                                            # ft.ElevatedButton(text="Salir", bgcolor="red", height=35, width=65, on_click=lambda _: page.go("/")),
                                            # ft.Text("Gestion", width=380, size=30, text_align="Left", weight="w900"),
                                        ]
                                    ),
                                    ft.padding.only(20, 20, 0, 0)
                                ),
                                ft.Container(
                                    ft.Tabs(
                                    selected_index=1,
                                    animation_duration=300,
                                    tabs=[
                                        ft.Tab(
                                            text="Pedidos",
                                            icon=ft.Icons.ADD_BOX,
                                            content= ft.Container(
                                                ft.Column(
                                                    [
                                                        ft.Text("Datos del Pedido", weight="w700", size=30),
                                                        ft.Container(
                                                            ft.TextField(width=350, hint_text="Ingrese ID del Pedido", color="white", prefix_icon= ft.icons.CARD_TRAVEL),
                                                        ),
                                                        ft.Container(
                                                            ft.TextField(width=350, hint_text="Ingrese su Contraseña", color="white", prefix_icon= ft.icons.LOCK, password=True, can_reveal_password=True),
                                                        )
                                                    ]
                                                ),
                                                ft.padding.only(20, 20, 0, 0)
                                            )
                                        ),
                                        ft.Tab(
                                            text="Trabajadores",
                                            icon=ft.Icons.PERSON
                                        ),
                                        ft.Tab(
                                            text="Camiones",
                                            icon=ft.Icons.FIRE_TRUCK
                                        ),
                                    ],
                                    expand=1,
                                    ),
                                    ft.padding.only(20, 0, 20, 20),
                                )
                            ]),
                            border_radius=8,
                            width=1170,
                            height=740,
                            bgcolor="#673AB7",
                        ),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)