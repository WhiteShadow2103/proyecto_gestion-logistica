import flet as ft
import pymysql as BD
import datetime as dt

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

def main(page: ft.Page):
    page.title = "SecuryCargo"
    page.window.width = 420
    page.window.height = 590

    def VerificarConexion(conn):
        try:
            conn.ping(reconnect=True)  # Verifica si la conexión está activa
            print("Conexión exitosa a la base de datos.")      
            return True
        except BD.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            print("Intentando reconectar...")
            return False
    
    # --- Funcion del Tab del Usuario --- #
    def BuscarTrabajoUsuario(codTrabajo):
        print("Bucle establecido")
        if codTrabajo == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe ingresar un código de trabajo."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
        else: 
            conn = conectar()
            cur = conn.cursor()
            origen = cur.execute("SELECT id_origen FROM guia WHERE id_guia = %s", (codTrabajo,))
            destino = cur.execute("SELECT id_destino FROM guia WHERE id_guia = %s", (codTrabajo,))
            #fecha = cur.execute("SELECT fecha FROM guia WHERE id_guia = %s", (codTrabajo,))
            conn.commit()
            dgl = ft.AlertDialog(title=ft.Text("Busqueda lograda:"), content=ft.Text("El trabajo tiene como origen {} y como destino {}. \n Debe ser entregado maximo en la fecha {}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            cur.close()
            conn.close()
            codTrabajo.value = ""
            page.update()  
    
    # --- Funciones del Tab Conductores --- #
    def AgregarConductorAd(rut, nombre, apellido):
        if rut == "" or nombre == "" or apellido == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe completar todos los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("INSERT INTO conductor (rut, nombre, apellido) VALUES (%s, %s, %s)", (rut, nombre, apellido,))
                dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Conductor agregado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                page.open(dgl)
                conn.commit()
                page.update()
            except BD.Error as e:
                dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo agregar el conductor: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                page.open(dgl)
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
            page.open(dgl)
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
            page.open(dgl)
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("UPDATE conductor SET nombre = %s, apellido = %s WHERE rut = %s", (nombre, apellido, rut,))
                dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Conductor modificado correctamente."), alignment=ft.alignment.center, on_dismiss=lambda e: print("Dialog dismissed!"), title_padding=ft.padding.all(25))
                page.open(dgl)
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
            page.open(dgl)
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
            ft.DataColumn(ft.Text("Código ID", size=18, weight="w700")),
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

    # --- Funciones del Tab Trabajos --- #

    def AgregarTrabajoAd(codigo, origen, destino, fecha, estado):
        if codigo == "" or origen == "" or destino == "" or fecha == "" or estado == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe completar todos los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO guia (id_guia, id_origen, id_destino, fecha, estado) VALUES (%s, %s, %s, %s, %s)", (codigo, origen, destino, fecha, estado,))
            dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Trabajo agregado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            conn.commit()
            page.update()
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo agregar el trabajo: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        finally:
            cur.close()
            conn.close()
            LimpiarCamposTrabajos()
            Recargar_TablaTrabajos()
            page.update()

    def EliminarTrabajoAd(codigo):
        if codigo == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("No pueden estar vacios los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM guia WHERE id_guia = %s", (codigo,))
            dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Trabajo eliminado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            conn.commit()
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo eliminar el trabajo: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        finally:
            cur.close()
            conn.close()
            codigoTrabajo.value = ""
            Recargar_TablaTrabajos()
            page.update()
            
    def ModificarTrabajoAd(codigo, origen, destino, fecha, estado):
        if codigo == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("No pueden estar vacios los campos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("UPDATE guia SET id_origen = %s, id_destino = %s, fecha = %s, estado = %s WHERE id_guia = %s", (origen, destino, fecha, estado, codigo,))
            dgl = ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text("Trabajo modificado correctamente."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            conn.commit()
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo modificar el trabajo: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        finally:
            cur.close()
            conn.close()
            LimpiarCamposTrabajos()
            Recargar_TablaTrabajos()
            page.update()

    tabla_Trabajos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Origen", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Destino", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Fecha de Entrega", size=18, weight="w700")),
            ft.DataColumn(ft.Text("Estado", size=18, weight="w700"))
        ],
    rows=[])
    def Recargar_TablaTrabajos():
        tabla_Trabajos.rows.clear()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT id_guia, id_origen, id_destino, fecha, estado FROM guia")
            resultados = cur.fetchall()
            for row in resultados:
                tabla_Trabajos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[0])),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2])),
                            ft.DataCell(ft.Text(row[3])),
                            ft.DataCell(ft.Text(row[4])),
                        ]
                    )
                )
        except BD.Error as e:
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo cargar la tabla de trabajos: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            dgl.open = True
            page.update()
        finally:
            cur.close()
            conn.close()
            page.update()

    def LimpiarCamposTrabajos():
        codigoTrabajo.value = ""
        lugarOrigen.value = ""
        lugarDestino.value = ""
        estadoTrabajo.value = ""
        fechaEntrega_text.value = ""
        page.update()

    # --- Funcion para el Login Admin --- #
    def IngresarAdmin(e):
        if rutAdmin.value == "admin" and contraseña.value == "admin":
            rutAdmin.value = ""
            contraseña.value = ""
            page.go("/principalAdmin")
            Recargar_TablaConductores()
            Recargar_TablaCamiones()
            Recargar_TablaTrabajos()
        else:
            dgl = ft.AlertDialog(title=ft.Text("No se pudo ingresar!!"), content=ft.Text("Es probable que el rut o la contraseña no sean correctos."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
            
    # --- Funcion para el Login Usuarios --- #
    def IngresarUsuario(e):
        if rut.value == "":
            dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Debe ingresar su Rut."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
            page.open(dgl)
            page.update()
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute("SELECT * FROM conductor WHERE rut = %s", (rut.value,))
                resultado = cur.fetchone()

                if resultado is not  None:
                    cantidad = int(resultado[0])
                    if cantidad > 0:
                        rut.value = ""
                        page.go("/principalUsuario")
                        Recargar_TablaTrabajos()
                    else:
                        dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Credenciales no Validas"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                        page.open(dgl)
                        page.update()
                else:
                    dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Rut no encontrado."), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                    page.open(dgl)
                    page.update()
            except BD.Error as e:
                dgl = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(f"No se pudo conectar a la base de datos: {e}"), alignment=ft.alignment.center, title_padding=ft.padding.all(25))
                page.open(dgl)
                page.update()
            finally:
                cur.close()
                conn.close()
                rut.value = ""
                page.update()

    # --- Control del Boton de Fecha --- #
    fechaEntrega_picker = ft.DatePicker(first_date=dt.date(2024, 1, 1), last_date=dt.date(2035, 12, 31))
    fechaEntrega_text = ft.TextField( width=350, hint_text="Ingrese Fecha de Entrega", color="white", prefix_icon= ft.Icons.CALENDAR_MONTH, read_only=True, disabled=True)
    page.overlay.append(fechaEntrega_picker)
    def abrir_fecha_picker(e):
        fechaEntrega_picker.open = True
        page.update()
    btn_abrir_fecha = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, icon_color="#FFFFFF", icon_size=40, tooltip="Seleccionar Fecha", on_click=abrir_fecha_picker)
    def actualizar_fecha_text(e):
        fechaEntrega_text.value = str(fechaEntrega_picker.value) or ""
        page.update()
    fechaEntrega_picker.on_change = actualizar_fecha_text

    # Variables de los texfield del Login de Usuario y de Administrador #
    rut = ft.TextField(width=350, hint_text="Ingrese Id de Usuario", color="white", prefix_icon= ft.Icons.PERSON)
    btn_LoginUsuario = ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=IngresarUsuario, disabled=True)
    btn_LoginAdmin = ft.TextButton(text="Ingresar como Admin", disabled= True,on_click=lambda e: page.go("/loginAdmin"))

    # Variables de los textfield del Login de Administrador #
    rutAdmin = ft.TextField(width=350, hint_text="Ingrese Id de Administrador", color="white", prefix_icon= ft.Icons.PERSON)
    contraseña = ft.TextField(width=350, hint_text="Ingrese su Contraseña", color="white", prefix_icon= ft.Icons.LOCK, password=True, can_reveal_password=True)
    
    # Variables de C.R.U.D. para el Usuario #
    codTrabajo = ft.TextField(width=350, hint_text="Ingrese Código del Pedido", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    
    # Variables de C.R.U.D. para el Administrador #
    rutConductor = ft.TextField(width=350, hint_text="Ingrese ID del Conductor", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    nombreConductor = ft.TextField(width=350, hint_text="Ingrese su Nombre", color="white", prefix_icon= ft.Icons.LOCK)
    apellidoConductor = ft.TextField(width=350, hint_text="Ingrese su Apellido", color="white", prefix_icon= ft.Icons.LOCK)

    patenteCamiones = ft.TextField(width=350, hint_text="Ingrese Patente del Camión", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    modeloCamiones = ft.TextField(width=350, hint_text="Ingrese Modelo del Camión", color="white", prefix_icon= ft.Icons.LOCK)
    marcaCamiones = ft.TextField(width=350, hint_text="Ingrese Marca del Camión", color="white", prefix_icon= ft.Icons.LOCK)

    codigoTrabajo = ft.TextField(width=350, hint_text="Ingrese Código de la Entrega", color="white", prefix_icon= ft.Icons.CARD_TRAVEL)
    lugarOrigen = ft.TextField(width=350, hint_text="Ingrese Origen", color="white", prefix_icon= ft.Icons.LOCK)
    lugarDestino= ft.TextField(width=350, hint_text="Ingrese Destino", color="white", prefix_icon= ft.Icons.LOCK)
    estadoTrabajo = ft.TextField(width=350, hint_text="Ingrese Estado de Entrega", color="white", prefix_icon= ft.Icons.LOCK)

    btn_cancelar = ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121", on_click=lambda e: LimpiarCamposConductores())

    # VISTAS (puedes separarlas luego en archivos)

    def loginUsuario():
        page.title = "SecuryCargo"
        page.window.width = 420
        page.window.height = 590
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Container(ft.Text("Iniciar Sesión", width=380, size=30, text_align="center", weight="w900"),ft.padding.only(10, 120, 0, 20)),
                        ft.Container(rut, padding=20),
                        ft.Container(btn_LoginUsuario, ft.padding.only(50, 30)),
                        ft.Container(ft.Row([ft.Container(btn_LoginAdmin, padding=ft.padding.only(110)), ft.Container(ft.IconButton(icon=ft.Icons.REFRESH, icon_color="#6CBEED", icon_size=20, tooltip="Reintentar Conexión"))]))
                    ]),
                    border_radius=8,
                    width=400,
                    height=530,
                    gradient=ft.LinearGradient(colors=["#38405F", "#59546C"])
                ),
            ]
        )

    def loginAdmin():
        page.title = "SecuryCargo"
        page.window.width = 420
        page.window.height = 590
        return ft.View(
            route="/login_admin",
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Container(ft.Text("Iniciar Sesión Administrador", width=380, size=30, text_align="center", weight="w900"), ft.padding.only(10, 50, 0, 20)),                            ft.Container(rutAdmin, padding=20),
                        ft.Container(contraseña, padding=20),
                        ft.Container(ft.ElevatedButton(text="Ingresar", width=280, height=40, bgcolor="#212121", on_click=IngresarAdmin),ft.padding.only(50, 30)),
                        ft.Container(ft.TextButton(text="Salir", on_click=lambda e: page.go("/")), ft.padding.only(160))
                    ]),
                    border_radius=8,
                    width=400,
                    height=530,
                    gradient=ft.LinearGradient(colors=["#38405F","#59546C"])
                )
            ]
        )

    def principalUsuario():
        page.title = "SecuryCargo"
        page.window.width = 1200
        page.window.height = 800
        return ft.View(
            route="/principalUsuario",
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Container(
                            ft.Row([                                    
                                ft.Container(content=ft.Text("Salir"), margin=10, padding=10, alignment=ft.alignment.center, bgcolor=ft.Colors.RED, width=65, height=40, border_radius=10, ink=True, on_click=lambda _: page.go("/")), 
                                ft.Container(content=ft.Text("Gestión Interna", weight="w900", size=18), margin=1, padding=1, alignment=ft.alignment.center_left, width=350, height=40)
                                ]), 
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
                                                ft.Container(ft.Text("Datos de los Trabajos", weight="w700", size=30)),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(codTrabajo),
                                                        ft.Container(ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121", on_click=lambda e: BuscarTrabajoUsuario(codTrabajo.value))),
                                                        ft.Container(ft.IconButton(icon=ft.Icons.REFRESH, icon_color="#FFFFFF", icon_size=30, tooltip="Recargar Tabla", on_click=lambda e: Recargar_TablaTrabajos()))
                                                    ])
                                                ),
                                                ft.Container(
                                                    ft.Text("Tabla de Trabajos", weight="w700", size=30),
                                                    ft.padding.only(0, 20, 0, 0)
                                                ),
                                                ft.Container(
                                                    content=ft.ListView(
                                                        controls=[tabla_Trabajos],
                                                        expand=True,  
                                                        height=340,   
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
                    gradient=ft.LinearGradient(colors=["#38405F","#59546C"])
                ),
            ]
        )

    def principalAdmin():
        page.title = "SecuryCargo"
        page.window.width = 1200
        page.window.height = 800
        return ft.View(
            route="/principalAdmin",
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Container(
                            ft.Row([
                                    ft.Container(content=ft.Text("Salir"), margin=10, padding=10, alignment=ft.alignment.center, bgcolor=ft.Colors.RED, width=65, height=40, border_radius=10, ink=True, on_click=lambda _: page.go("/loginAdmin")),
                                    ft.Container(content=ft.Text("Gestión Interna", weight="w900", size=18), margin=1, padding=1, alignment=ft.alignment.center_left, width=350, height=40) 
                                ]),
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
                                                ft.Container(ft.Text("Datos de los Trabajos", weight="w700", size=30),),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(codigoTrabajo),
                                                        ft.Container(lugarOrigen),
                                                        ft.Container(lugarDestino)
                                                    ])
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(estadoTrabajo),
                                                        ft.Container(ft.Column([fechaEntrega_text])),
                                                        ft.Container(btn_abrir_fecha, padding=ft.padding.only(10, 0, 0, 0))
                                                    ]),
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121",  on_click=lambda e: AgregarTrabajoAd(codigoTrabajo.value, lugarOrigen.value, lugarDestino.value, fechaEntrega_picker.value, estadoTrabajo.value))),
                                                        ft.Container(ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", on_click=lambda e: ModificarTrabajoAd(codigoTrabajo.value, lugarOrigen.value, lugarDestino.value, fechaEntrega_picker.value, estadoTrabajo.value)))
                                                    ]),
                                                    ft.padding.only(70)
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", on_click=lambda e: EliminarTrabajoAd(codigoTrabajo.value))),
                                                        ft.Container(ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121", on_click=lambda e: LimpiarCamposTrabajos())),
                                                    ]),
                                                    ft.padding.only(170),
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.Text("Tabla de Trabajos", weight="w700", size=30)),
                                                        ft.Container(ft.IconButton(icon=ft.Icons.REFRESH, icon_color="#FFFFFF", icon_size=30, tooltip="Recargar Tabla", on_click=lambda e: Recargar_TablaTrabajos()))
                                                    ])
                                                ),
                                                ft.Container(
                                                    content=ft.ListView(
                                                        controls=[tabla_Trabajos],
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
                                    icon=ft.Icons.PERSON_ADD,
                                    content= ft.Container(
                                        ft.Column(
                                            [
                                                ft.Container(ft.Text("Datos de los Conductores", weight="w700", size=30),),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(rutConductor),
                                                        ft.Container(nombreConductor),
                                                        ft.Container(apellidoConductor),
                                                    ])
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", on_click=lambda e: AgregarConductorAd(rutConductor.value, nombreConductor.value, apellidoConductor.value))),
                                                        ft.Container(ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", on_click=lambda e: ModificarConductorAd(rutConductor.value, nombreConductor.value, apellidoConductor.value)))
                                                    ]),
                                                    ft.padding.only(250)
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", on_click=lambda e: EliminarConductorAd(rutConductor.value))),
                                                        ft.Container(btn_cancelar)
                                                    ]),
                                                    ft.padding.only(350),
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.Text("Tabla de Conductores", weight="w700", size=30)),
                                                        ft.Container(ft.IconButton(icon=ft.Icons.REFRESH, icon_color="#FFFFFF", icon_size=30, tooltip="Recargar Tabla", on_click=lambda e: Recargar_TablaTrabajos()))
                                                    ])
                                                ),
                                                ft.Container(
                                                    content=ft.ListView(
                                                        controls=[tabla_conductores],
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
                                    icon=ft.Icons.FIRE_TRUCK,
                                    content= ft.Container(
                                        ft.Column(
                                            [
                                                ft.Container(ft.Text("Datos de los Camiones", weight="w700", size=30)),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(patenteCamiones),
                                                        ft.Container(marcaCamiones),
                                                        ft.Container(modeloCamiones)
                                                    ])
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.ElevatedButton(text="Agregar", width=280, height=40, bgcolor="#212121", on_click=lambda e: AgregarCamionesAd(patenteCamiones.value, modeloCamiones.value, marcaCamiones.value))),
                                                        ft.Container(ft.ElevatedButton(text="Modificar", width=280, height=40, bgcolor="#212121", on_click=lambda e: ModificarCamionesAd(patenteCamiones.value, modeloCamiones.value, marcaCamiones.value))),
                                                        ft.Container(ft.ElevatedButton(text="Buscar", width=80, height=40, bgcolor="#212121"))
                                                    ]),
                                                    ft.padding.only(200)
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.ElevatedButton(text="Eliminar", width=280, height=40, bgcolor="#212121", on_click=lambda e: EliminarCamionesAd(patenteCamiones.value))),
                                                        ft.Container(ft.ElevatedButton(text="Cancelar", width=80, height=40, bgcolor="#212121" , on_click=lambda e: LimpiarCamposCamiones())),
                                                    ]),
                                                    ft.padding.only(350),
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        ft.Container(ft.Text("Tabla de Camiones", weight="w700", size=30)),
                                                        ft.Container(ft.IconButton(icon=ft.Icons.REFRESH, icon_color="#FFFFFF", icon_size=30, tooltip="Recargar Tabla", on_click=lambda e: Recargar_TablaTrabajos()))
                                                    ])
                                                ),
                                                ft.Container(
                                                    content=ft.ListView(
                                                        controls=[tabla_Camiones],
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
                    gradient=ft.LinearGradient(colors=["#38405F","#59546C"])
                ),
            ]
        )

    # --- Navegación entre vistas --- #
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(loginUsuario())
            page.update()
        elif page.route == "/loginAdmin":
            page.views.append(loginAdmin())
            page.update()
        elif page.route == "/principalUsuario":
            page.views.append(principalUsuario())
            page.update()
        elif page.route == "/principalAdmin":
            page.views.append(principalAdmin())
            page.update()
        else:
            page.views.append(ft.View("/", [ft.Text("Ruta no encontrada")]))
        page.update()

    page.on_route_change = route_change
    page.route = "/"
    route_change(None)

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
