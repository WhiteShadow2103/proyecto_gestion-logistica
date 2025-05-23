import flet as ft

def main(page: ft.Page):
   
    def route_change(route):
        page.views.clear()
        page.window.width = 420
        page.window.height = 590
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.title = "SecuryCargo"
        page.views.append(
            ft.View(
                "/",
                [
                ft.Container(
                    ft.Column([
                        ft.Container(
                            ft.Text("Iniciar Sesión", width=380, size=30, text_align="center", weight="w900"),
                            ft.padding.only(10, 100, 0, 20)
                        ),
                        ft.Container(
                            ft.TextField(width=350, hint_text="Ingrese su Rut", color="white", prefix_icon= ft.icons.PERSON),
                            ft.padding.only(20),
                            
                        ),
                        ft.Container(
                            ft.TextField(width=350, hint_text="Ingrese su Contraseña", color="white", prefix_icon= ft.icons.LOCK, password=True, can_reveal_password=True),
                            ft.padding.only(20),
                        ),
                        ft.Container(
                            ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=lambda e: page.go("/principal")),
                            ft.padding.only(60, 30),
                        ),
                        ft.Container(
                            ft.TextButton(text="Crear Usuario", on_click=lambda e: page.go("/crearUser")),
                            ft.padding.only(150)
                        )
                    ]
                    ),
                        border_radius=8,
                        width=400,
                        height=530,
                        gradient=ft.LinearGradient(
                            colors=[
                                "#673AB7",
                                "#512DA8",
                            ],
                        ),
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
                                            ),
                                            
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
                                            text="Trabajos",
                                            icon=ft.Icons.ADD_BOX,
                                            content= ft.Container(
                                                ft.Column(
                                                    [
                                                        ft.Container(
                                                            ft.Text("Datos de los Trabajos", weight="w700", size=30),
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Código del Pedido", color="white", prefix_icon= ft.icons.CARD_TRAVEL),
                                                                ),
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Origen", color="white", prefix_icon= ft.icons.LOCK, disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121")
                                                                )
                                                            ])
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Peso de la Carga", color="white", prefix_icon= ft.icons.LOCK, disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Destino", color="white", prefix_icon= ft.icons.LOCK, disabled=True),
                                                                )
                                                            ]),
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                )
                                                            ]),
                                                            ft.padding.only(70)
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Detalle", width=80, height=40, bgcolor="#212121"),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121"),
                                                                ),
                                                            ]),
                                                            ft.padding.only(120),
                                                        ),
                                                        ft.Container(
                                                           ft.Text("Tabla de Cargas", weight="w700", size=30),
                                                           ft.padding.only(0, 20, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.ListView(
                                                                controls=[
                                                                    ft.DataTable(
                                                                        columns=[
                                                                            ft.DataColumn(ft.Text("Código", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Origen", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Peso(kg)", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Destino", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Estado", size=18, weight="w700")),
                                                                        ],
                                                                        rows=[
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("001")),
                                                                                    ft.DataCell(ft.Text("Producto A")),
                                                                                    ft.DataCell(ft.Text("10")),
                                                                                    ft.DataCell(ft.Text("10")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("002")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("003")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("004")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("005")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("006")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("007")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("008")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("006")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("En Espera")),
                                                                                ],
                                                                            ),
                                                                            # Agrega más filas aquí según sea necesario
                                                                        ],
                                                                    )
                                                                ],
                                                                expand=True,  # Permite que el ListView ocupe el espacio disponible
                                                                height=200,   # Altura fija para habilitar el scroll
                                                            ),
                                                        )
                                                    ]
                                                ),
                                                ft.padding.only(20, 20, 0, 0)
                                            )
                                        ),
                                        ft.Tab(
                                            text="Conductores",
                                            icon=ft.Icons.ADD_BOX,
                                            content= ft.Container(
                                                ft.Column(
                                                    [
                                                        ft.Container(
                                                            ft.Text("Datos de los Conductores", weight="w700", size=30),
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Rut del Conductor", color="white", prefix_icon= ft.icons.CARD_TRAVEL),
                                                                ),
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese su Nombre", color="white", prefix_icon= ft.icons.LOCK, disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121")
                                                                )
                                                            ])
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Patente Asignada", color="white", prefix_icon= ft.icons.LOCK, disabled=True),
                                                                )
                                                            ]),
                                                            ft.padding.only(180)
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                )
                                                            ]),
                                                            ft.padding.only(70)
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Detalle", width=80, height=40, bgcolor="#212121"),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121"),
                                                                ),
                                                            ]),
                                                            ft.padding.only(120),
                                                        ),
                                                        ft.Container(
                                                           ft.Text("Tabla de Conductores", weight="w700", size=30),
                                                           ft.padding.only(0, 20, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.ListView(
                                                                controls=[
                                                                    ft.DataTable(
                                                                        columns=[
                                                                            ft.DataColumn(ft.Text("Código", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Nombre", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Rut", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Patente Asignada", size=18, weight="w700")),
                                                                        ],
                                                                        rows=[
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("001")),
                                                                                    ft.DataCell(ft.Text("Producto A")),
                                                                                    ft.DataCell(ft.Text("10")),
                                                                                    ft.DataCell(ft.Text("10"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("002")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("003")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("004")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("005")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("006")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("007")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("008")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("006")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                    ft.DataCell(ft.Text("20"))
                                                                                ],
                                                                            ),
                                                                            # Agrega más filas aquí según sea necesario
                                                                        ],
                                                                    )
                                                                ],
                                                                expand=True,  # Permite que el ListView ocupe el espacio disponible
                                                                height=200,   # Altura fija para habilitar el scroll
                                                            ),
                                                        )
                                                    ]
                                                ),
                                                ft.padding.only(20, 20, 0, 0)
                                            )
                                        ),
                                        ft.Tab(
                                            text="Camiones",
                                            icon=ft.Icons.ADD_BOX,
                                            content= ft.Container(
                                                ft.Column(
                                                    [
                                                        ft.Container(
                                                            ft.Text("Datos de los Camiones", weight="w700", size=30),
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Patente del Camión", color="white", prefix_icon= ft.icons.CARD_TRAVEL),
                                                                ),
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Modelo del Camión", color="white", prefix_icon= ft.icons.LOCK, disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121")
                                                                )
                                                            ])
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                )
                                                            ]),
                                                            ft.padding.only(70)
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121"),
                                                                ),
                                                            ]),
                                                            ft.padding.only(160),
                                                        ),
                                                        ft.Container(
                                                           ft.Text("Tabla de Camiones", weight="w700", size=30),
                                                           ft.padding.only(0, 20, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.ListView(
                                                                controls=[
                                                                    ft.DataTable(
                                                                        columns=[
                                                                            ft.DataColumn(ft.Text("Id del Camión", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Modelo", size=18, weight="w700")),
                                                                            ft.DataColumn(ft.Text("Patente", size=18, weight="w700")),
                                                                        ],
                                                                        rows=[
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("001")),
                                                                                    ft.DataCell(ft.Text("Producto A")),
                                                                                    ft.DataCell(ft.Text("10")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("002")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("003")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("004")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("005")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("006")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("007")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            ft.DataRow(
                                                                                cells=[
                                                                                    ft.DataCell(ft.Text("008")),
                                                                                    ft.DataCell(ft.Text("Producto B")),
                                                                                    ft.DataCell(ft.Text("20")),
                                                                                ],
                                                                            ),
                                                                            # Agrega más filas aquí según sea necesario
                                                                        ],
                                                                    )
                                                                ],
                                                                expand=True,  # Permite que el ListView ocupe el espacio disponible
                                                                height=200,   # Altura fija para habilitar el scroll
                                                            ),
                                                        )
                                                    ]
                                                ),
                                                ft.padding.only(20, 20, 0, 0)
                                            )
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
                            gradient=ft.LinearGradient(
                            colors=[
                                "#673AB7",
                                "#003249",
                            ],
                        ),
                        ),
                    ],
                )
            )
        elif page.route == "/crearUser":
            page.window.width = 420
            page.window.height = 590
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.views.append(
                ft.View(
                    "/crearUser",
                    [
                        ft.Container(
                                ft.Column([
                                    ft.Container(
                                        ft.Text("Crear Usuario", width=380, size=30, text_align="center", weight="w900"),
                                        ft.padding.only(10, 100, 0, 20)
                                    ),
                                    ft.Container(
                                        ft.TextField(width=350, hint_text="Ingrese Nombre de Usuario", color="white", prefix_icon= ft.icons.PERSON),
                                        ft.padding.only(20),
                                    ),
                                    ft.Container(
                                        ft.TextField(width=350, hint_text="Ingrese Run del Usuario", color="white", prefix_icon= ft.icons.LOCK, password=True, can_reveal_password=True),
                                        ft.padding.only(20),
                                    ),
                                    ft.Container(
                                        ft.TextField(width=350, hint_text="Ingrese una Contraseña", color="white", prefix_icon= ft.icons.LOCK, password=True, can_reveal_password=True),
                                        ft.padding.only(20),
                                    ),
                                    ft.Container(
                                        ft.ElevatedButton(text="Crear Usuario", width=280, height=40, bgcolor="#212121", on_click=lambda e: page.go("/")),
                                        ft.padding.only(60, 30),
                                    ),
                                    ft.Container(
                                        content=ft.Text("Salir"),
                                        margin=10,
                                        padding=10,
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.Colors.RED,
                                        width=65,
                                        height=40,
                                        border_radius=20,
                                        ink=True,
                                        on_click=lambda _: page.go("/"), 
                                    ),
                                ]
                            ),
                            border_radius=8,
                            width=400,
                            height=530,
                            gradient=ft.LinearGradient(
                            colors=[
                                "#673AB7",
                                "#512DA8",
                            ],
                        ),
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