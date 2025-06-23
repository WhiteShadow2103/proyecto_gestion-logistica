import flet as ft
import pymysql as BD

# Configuraciones de la conexion a la Base de Datos #
def conectar():
    try:
        return BD.connect(
            host='localhost',
            user='root',
            password='',
            database='securycargo',
            port=3306
        )
    except BD.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Funciones principales de la aplicacion #
def main(page: ft.Page):
    # Función para verificar la conexión a la base de datos #
    def VerificarConexion(conn):
        try:
            conn.ping(reconnect=True)  # Verifica si la conexión está activa
            return True
        except BD.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            return False

     # --- Funciones de la Base de Datos --- #
    
    # --- Funcion del Tab del Usuario --- #
    def BuscarTrabajoUsuario(codTrabajo):
        print("Bucle establecido")
        if codTrabajo == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe ingresar un código de trabajo."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
            page.open(dgl)
        else: 
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT * FROM trabajo WHERE codigo = %s", (codTrabajo,))
            print("Conexion conseguida")
            conn.commit()
            cur.close()
            conn.close()
            codTrabajo.value = ""
            page.update()  
    
    # --- Funciones del Tab Conductores --- #
    def AgregarConductorAd(rut, nombre, apellido):
        if rut == "" or nombre == "" or apellido == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe completar todos los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            dgl.open = True
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("INSERT INTO conductor (rut, nombre, apellido) VALUES (%s, %s, %s)", (rut, nombre, apellido,))
                dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Conductor agregado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                dgl.open = True
                conn.commit()
                page.update()
            except BD.Error as e:
                dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo agregar el conductor: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                dgl.open = True
                page.update()
            finally:
                cur.close()
                conn.close()
                LimpiarCamposConductores()
                Recargar_TablaConductores()
                page.update()

    def EliminarConductorAd(rut):
        if rut == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("No pueden estar vacios los campos."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
            dgl.open = True
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("DELETE FROM conductor WHERE rut = %s", (rut,))
                dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Conductor eliminado correctamente."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
                page.open(dgl)
                conn.commit()
            except BD.Error as e:
                dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo eliminar el conductor: {e}"), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
                page.open(dgl)
            finally:
                cur.close()
                conn.close()
                rutConductor.value = ""
                Recargar_TablaConductores()
                page.update()  

    def ModificarConductorAd(rut, nombre, apellido):
        if rut == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("No pueden estar vacios los campos."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
            dgl.opnen = True
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("UPDATE conductor SET nombre = %s, apellido = %s WHERE rut = %s", (nombre, apellido, rut,))
                dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Conductor modificado correctamente."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
                dgl.open = True
                conn.commit()
            except BD.Error as e:
                dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo Modificar el conductor: {e}"), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
                page.open(dgl)
            finally:
                cur.close()
                conn.close()
                LimpiarCamposConductores()
                Recargar_TablaConductores()
                page.update()

    tabla_conductores = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Rut", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Nombre", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Apellido", size=18, weight="w700"))
        ],
    rows=[])
    def Recargar_TablaConductores():
        tabla_conductores.rows.clear()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT rut, nombre, apellido FROM conductor")
            resultados = cur.fetchall()
            for row in resultados:
                tabla_conductores.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[0])),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2])),
                        ]
                    )
                )
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo cargar la tabla de conductores: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        finally:
            cur.close()
            conn.close()
            page.update()

    def LimpiarCamposConductores():
        rutConductor.value = ""
        nombreConductor.value = ""
        apellidoConductor.value = ""
        page.update()

    # --- Funciones del Tab Camiones --- #
    def AgregarCamionesAd(patente, modelo, marca):
        if patente == "" or modelo == "" or marca == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe completar todos los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            dgl.open = True
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("INSERT INTO camion (patente, modelo, marca) VALUES (%s, %s, %s)", (patente, modelo, marca,))
                dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Camión agregado correctamente."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
                page.open(dgl)
                conn.commit()
                page.update()
            except BD.Error as e:
                dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo agregar el camión: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                page.open(dgl)
                page.update()
            finally:
                cur.close()
                conn.close()
                LimpiarCamposCamiones()
                Recargar_TablaCamiones()
                page.update()

    def EliminarCamionesAd(patente):
        if patente == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("No pueden estar vacios los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM camion WHERE patente = %s", (patente,))
            dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Camión eliminado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            conn.commit()
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo eliminar el camión: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
        finally:
            cur.close()
            conn.close()
            patenteCamiones.value = ""
            Recargar_TablaCamiones()
            page.update()

    def ModificarCamionesAd(patente, modelo, marca):
        if patente == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("No pueden estar vacios los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("UPDATE camion SET modelo = %s, marca = %s WHERE patente = %s", (modelo, marca, patente,))
            dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Camión modificado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            conn.commit()
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo modificar el camión: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
        finally:
            cur.close()
            conn.close()
            Recargar_TablaCamiones()
            page.update()

    tabla_Camiones = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Patente", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Marca", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Modelo", size=18, weight="w700"))
        ],
    rows=[])
    def Recargar_TablaCamiones():
        tabla_Camiones.rows.clear()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT patente, marca, modelo FROM camion")
            resultados = cur.fetchall()
            for row in resultados:
                tabla_Camiones.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[0])),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2])),
                        ]
                    )
                )
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo cargar la tabla de camiones: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            dgl.open = True
            page.update()
        finally:
            cur.close()
            conn.close()
            page.update()

    def LimpiarCamposCamiones():
        patenteCamiones.value = ""
        modeloCamiones.value = ""
        marcaCamiones.value = ""
        page.update()

    # --- Funcion para el Login Admin --- #
    def IngresarAdmin(e):
        if rutAdmin.value == "21386644-3" and contraseña.value == "1234":
            rutAdmin.value = ""
            contraseña.value = ""
            page.go("/principalAdmin")
        else:
            dgl = ft.AlertDialog(title=ft.Text("No se pudo ingresar!!"), content=ft.Text("Es probable que el rut o la contraseña no sean correctos."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
            
    # --- Funcion para el Login Usuarios --- #
    def IngresarUsuario(e):
        if rut.value == "21386644-3":
            rut.value = ""
            page.go("/principalUsuarios")
        else:
            dgl = ft.AlertDialog(title=ft.Text("No se pudo ingresar!!"), content=ft.Text("Es probable que el rut no sea correctos."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
            dgl.open = True
            page.update()

    # Variables de los texfield del Login de Usuario y de Administrador #
    rut = ft.TextField(width=350, hint_text="Ingrese su Rut", color="white", prefix_icon= ft.Icons.PERSON)
    btn_LoginUsuario = ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=IngresarUsuario, disabled=True)
    btn_LoginAdmin = ft.TextButton(text="Ingresar como Admin", disabled= True,on_click=lambda e: page.go("/loginAdmin"))

    # Variables de los textfield del Login de Administrador #
    rutAdmin = ft.TextField(width=350, hint_text="Ingrese su Rut", color="white", prefix_icon= ft.Icons.PERSON)
    contraseña = ft.TextField(width=350, hint_text="Ingrese su Contraseña", color="white", prefix_icon= ft.Icons.LOCK, password=True, can_reveal_password=True)
    
    # Variables de C.R.U.D. para el Usuario #
    codTrabajo = ft.TextField(width=350, hint_text="Ingrese Código del Pedido", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    
    # Variables de C.R.U.D. para el Administrador #
    rutConductor = ft.TextField(width=350, hint_text="Ingrese Rut del Conductor", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    nombreConductor = ft.TextField(width=350, hint_text="Ingrese su Nombre", color="white", prefix_icon= ft.Icons.LOCK)
    apellidoConductor = ft.TextField(width=350, hint_text="Ingrese su Apellido", color="white", prefix_icon= ft.Icons.LOCK)

    patenteCamiones = ft.TextField(width=350, hint_text="Ingrese Patente del Camión", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    modeloCamiones = ft.TextField(width=350, hint_text="Ingrese Modelo del Camión", color="white", prefix_icon= ft.Icons.LOCK)
    marcaCamiones = ft.TextField(width=350, hint_text="Ingrese Marca del Camión", color="white", prefix_icon= ft.Icons.LOCK)

    btn_cancelar = ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121", on_click=lambda e: LimpiarCamposConductores())
             
    # Aplicación principal #
    def route_change(route):
        # Login del Usuario
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
                            ft.padding.only(10, 120, 0, 20)
                        ),
                        ft.Container(rut, padding=20),
                        ft.Container(
                            btn_LoginUsuario,
                            ft.padding.only(60, 30),
                        ),
                        ft.Container(
                            btn_LoginAdmin,
                            ft.padding.only(120)
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
        # Login del Administrador
        if page.route == "/loginAdmin":
            page.window.width = 420
            page.window.height = 590
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.title = "SecuryCargo"
            page.views.append(
                ft.View(
                    "/loginAdmin",
                    [
                    ft.Container(
                        ft.Column([
                            ft.Container(
                                ft.Text("Iniciar Sesión Administrador", width=380, size=30, text_align="center", weight="w900"),
                                ft.padding.only(10, 50, 0, 20)
                            ),
                            ft.Container(rutAdmin, padding=20),
                            ft.Container(contraseña, padding=20),
                            ft.Container(
                                ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=IngresarAdmin),
                                ft.padding.only(60, 30),
                            ),
                            ft.Container(
                                ft.TextButton(text="Salir", on_click=lambda e: page.go("/")),
                                ft.padding.only(170)
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
        # Ventana Principal del Administrador
        elif page.route == "/principalAdmin":
            Recargar_TablaConductores()
            Recargar_TablaCamiones()
            page.window.width = 1200
            page.window.height = 800
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.views.append(
                ft.View(
                    "/principalAdmin",
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
                                                on_click=lambda _: page.go("/loginAdmin"), 
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
                                                                    ft.TextField(width=350, hint_text="Ingrese Código del Pedido", color="white", prefix_icon= ft.Icons.CARD_TRAVEL),
                                                                ),
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Origen", color="white", prefix_icon= ft.Icons.LOCK, disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121")
                                                                )
                                                            ])
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Peso de la Carga", color="white", prefix_icon= ft.Icons.LOCK, disabled=True),
                                                                ),
                                                                ft.Container(
                                                                    ft.TextField(width=350, hint_text="Ingrese Destino", color="white", prefix_icon= ft.Icons.LOCK, disabled=True),
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
                                                                ft.Container(rutConductor),
                                                                ft.Container(nombreConductor),
                                                                ft.Container(apellidoConductor),
                                                            ])
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", on_click=lambda e: AgregarConductorAd(rutConductor.value, nombreConductor.value, apellidoConductor.value)),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", on_click=lambda e: ModificarConductorAd(rutConductor.value, nombreConductor.value, apellidoConductor.value)),
                                                                )
                                                            ]),
                                                            ft.padding.only(250)
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", on_click=lambda e: EliminarConductorAd(rutConductor.value)),
                                                                ),
                                                                ft.Container(
                                                                    btn_cancelar
                                                                ),
                                                            ]),
                                                            ft.padding.only(350),
                                                        ),
                                                        ft.Container(
                                                           ft.Text("Tabla de Conductores", weight="w700", size=30),
                                                           ft.padding.only(0, 20, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.ListView(
                                                                controls=[
                                                                    tabla_conductores
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
                                                                ft.Container(patenteCamiones),
                                                                ft.Container(marcaCamiones),
                                                                ft.Container(modeloCamiones)
                                                            ])
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", on_click=lambda e: AgregarCamionesAd(patenteCamiones.value, modeloCamiones.value, marcaCamiones.value)),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", on_click=lambda e: ModificarCamionesAd(patenteCamiones.value, modeloCamiones.value, marcaCamiones.value)),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121")
                                                                )
                                                            ]),
                                                            ft.padding.only(200)
                                                        ),
                                                        ft.Container(
                                                            ft.Row([
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", on_click=lambda e: EliminarCamionesAd(patenteCamiones.value)),
                                                                ),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121" , on_click=lambda e: LimpiarCamposCamiones()),
                                                                ),
                                                            ]),
                                                            ft.padding.only(350),
                                                        ),
                                                        ft.Container(
                                                           ft.Text("Tabla de Camiones", weight="w700", size=30),
                                                           ft.padding.only(0, 20, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.ListView(
                                                                controls=[
                                                                    tabla_Camiones
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
        # Ventana Principal de Usuarios
        elif page.route == "/principalUsuarios":
            page.window.width = 1200
            page.window.height = 800
            page.vertical_alignment = "center"
            page.horizontal_alignment = "center"
            page.views.clear()
            page.views.append(
                ft.View(
                    "/principalUsuarios",
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
                                                                ft.Container(codTrabajo),
                                                                ft.Container(
                                                                    ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121", on_click=lambda e: BuscarTrabajoUsuario(codTrabajo.value))
                                                                )
                                                            ])
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
                                                                                    ft.DataCell(ft.Text("009")),
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
                                                                height=340,   # Altura fija para habilitar el scroll
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
        page.update()
    
    def view_pop(view):
        if page.views:
            page.views.pop()

        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    conn = conectar()
    if not conn or not VerificarConexion(conn):
        btn_LoginUsuario.disabled = True
        btn_LoginAdmin.disabled = True
        page.update()
    else:
        btn_LoginUsuario.disabled = False
        btn_LoginAdmin.disabled = False
        page.update()

ft.app(target=main)