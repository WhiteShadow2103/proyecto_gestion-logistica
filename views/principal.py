import flet as ft

def principal_menu(page: ft.Page):

    page.view.append(
        ft.View(
            route="/principal_menu",
            controls=[
                ft.text(""),
            ]
        )
    )

    page.window.width = 1200
    page.window.height = 800
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.title = "StormCargoGest"

    page.add(
        ft.Container(
            ft.Column([
                ft.Container(
                    ft.ElevatedButton(text="Salir", bgcolor="red", height=40),
                    ft.padding.only(1090, 20, 0, 0 )
                ),
                ft.Container(
                    ft.Tabs(
                    selected_index=1,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="Pedidos",
                            icon=ft.Icons.ADD_BOX,
                            content= ft.TextField(label="Standard")
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
            border_radius=20,
            width=1170,
            height=740,
            bgcolor="#673AB7",
        )
    )

ft.app(target=principal_menu)