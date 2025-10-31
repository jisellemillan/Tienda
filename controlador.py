# Importamos los tipos para los "type hints"
from modelo.modelo_logica import ModeloLogica
from vista.vista_tk import VistaPrincipal
from modelo.excepciones import CantidadInvalidaError, ArticuloNoEncontradoError, ClienteNoEncontradoError, PrecioInvalidoError
from typing import Optional

class Controlador:
    """
    Conecta la vista con el modelo escucha los eventos de la vista (clics de boton) y actua sobre el modelo
    luego, le pide a la vista que se actualice
    """
    def __init__(self, modelo: ModeloLogica, vista: VistaPrincipal):
        self.modelo = modelo
        self.vista = vista
        # Conectamos los botones de la vista a metodos de este controlador
        self.asignar_controladores()
    
    def asignar_controladores(self) -> None:
        """Asigna los 'command' de los botones de la vista"""
        # Pestaña Clientes
        self.vista.btn_registrar_cliente.config(command=self.registrar_cliente)
        self.vista.btn_eliminar_cliente.config(command=self.eliminar_cliente)
        
        # Pestaña Articulos
        self.vista.btn_registrar_articulo.config(command=self.registrar_articulo)
        
        # Pestaña Facturacion
        self.vista.btn_nueva_factura.config(command=self.nueva_factura)
        self.vista.btn_agregar_linea.config(command=self.agregar_linea)
        self.vista.btn_eliminar_linea.config(command=self.eliminar_linea)
        self.vista.btn_exportar_json.config(command=self.exportar_json)
        self.vista.btn_exportar_csv.config(command=self.exportar_csv)

    def actualizar_listas_y_combos(self) -> None:
        """
        Metodo ayudante para actualizar todos los datos
        en la vista despues de un cambio en el modelo
        """
        clientes = self.modelo.clientes
        articulos = self.modelo.articulos
        self.vista.actualizar_lista_clientes(clientes)
        self.vista.actualizar_lista_articulos(articulos)
        self.vista.actualizar_combos(clientes, articulos)

    # Manejadores de eventos (Clientes) 

    def registrar_cliente(self) -> None:
        """Maneja el clic en el boton 'registrar cliente'"""
        try:
            # 1. Obtener datos de la Vista
            nombre = self.vista.entry_cliente_nombre.get()
            apellidos = self.vista.entry_cliente_apellidos.get()
            dni = self.vista.entry_cliente_dni.get()
            
            # 2. Validar datos
            if not nombre or not apellidos or not dni:
                raise ValueError("todos los campos son obligatorios")
            
            # 3. Llamar al Modelo
            self.modelo.registrar_cliente(nombre, apellidos, dni)
            
            # 4. Actualizar la Vista
            self.actualizar_listas_y_combos()
            
            # 5. Limpiar campos de entrada
            self.vista.entry_cliente_nombre.delete(0, 'end')
            self.vista.entry_cliente_apellidos.delete(0, 'end')
            self.vista.entry_cliente_dni.delete(0, 'end')
            
        except ValueError as e:
            # Si hay un error, mostrarlo
            self.vista.mostrar_error("error de validacion", str(e))

    def eliminar_cliente(self) -> None:
        """Maneja el clic en el boton 'eliminar cliente'"""
        try:
            # 1 Obtener seleccion del Treeview (tabla)
            seleccion = self.vista.tree_clientes.focus()
            if not seleccion:
                raise ValueError("debe seleccionar un cliente")
            
            item = self.vista.tree_clientes.item(seleccion)
            dni = item['values'][2] # El DNI esta en la tercera columna
            
            # 2 Llamar al Modelo
            self.modelo.eliminar_cliente(dni)
            
            # 3Actualizar la Vista
            self.actualizar_listas_y_combos()
            self.vista.actualizar_vista_factura(None) # Limpiar factura si se borra el cliente
            
        except (ValueError, ClienteNoEncontradoError) as e:
            self.vista.mostrar_error("error al eliminar", str(e))

    # Manejadores de eventos (Articulos) 

    def registrar_articulo(self) -> None:
        """Maneja el clic en el boton 'registrar articulo'"""
        try:
            # 1 Obtener datos de la Vista
            tipo = self.vista.tipo_articulo_var.get()
            codigo = self.vista.entry_articulo_codigo.get()
            denominacion = self.vista.entry_articulo_denominacion.get()
            precio_str = self.vista.entry_articulo_precio.get()
            extra = self.vista.entry_articulo_extra.get()

            # 2 Validar datos
            if not codigo or not denominacion or not precio_str or not extra:
                raise ValueError("todos los campos son obligatorios")
            
            precio = float(precio_str) # Puede lanzar ValueError

            # 3 Llamar al Modelo (segun el tipo)
            if tipo == "fisico":
                peso = float(extra) # Puede lanzar ValueError
                self.modelo.registrar_articulo_fisico(codigo, denominacion, precio, peso)
            else:
                licencia = extra
                self.modelo.registrar_articulo_digital(codigo, denominacion, precio, licencia)
            
            # 4 Actualizar la Vista
            self.actualizar_listas_y_combos()
            
            # 5 Limpiar campos
            self.vista.entry_articulo_codigo.delete(0, 'end')
            self.vista.entry_articulo_denominacion.delete(0, 'end')
            self.vista.entry_articulo_precio.delete(0, 'end')
            self.vista.entry_articulo_extra.delete(0, 'end')

        except (ValueError, PrecioInvalidoError) as e:
            # Capturamos error de conversion (float/int) o de precio
            self.vista.mostrar_error("error de validacion", str(e))

    #Manejadores de eventos (Facturacion) 

    def nueva_factura(self) -> None:
        """Maneja el clic en el boton 'nueva factura'."""
        try:
            # 1. Obtener cliente del Combobox
            dni_cliente = self.vista.combo_factura_cliente.get()
            if not dni_cliente:
                raise ValueError("debe seleccionar un cliente")
            
            # 2. Llamar al Modelo
            factura = self.modelo.crear_nueva_factura(dni_cliente)
            
            # 3. Actualizar la Vista (la seccion de factura)
            self.vista.actualizar_vista_factura(factura)
            
        except (ValueError, ClienteNoEncontradoError) as e:
            self.vista.mostrar_error("error", str(e))

    def agregar_linea(self) -> None:
        """Maneja el clic en 'agregar linea'."""
        try:
            # 1 Validar que hay una factura activa
            if not self.modelo.factura_actual:
                raise ValueError("primero debe crear una nueva factura")

            # 2 Obtener datos de la Vista
            codigo_articulo = self.vista.combo_factura_articulo.get()
            cantidad_str = self.vista.entry_factura_cantidad.get()

            if not codigo_articulo or not cantidad_str:
                raise ValueError("debe seleccionar un articulo y una cantidad")
            
            cantidad = int(cantidad_str) # Puede lanzar ValueError
            
            # 3 Llamar al Modelo
            self.modelo.agregar_linea_factura(codigo_articulo, cantidad)
            
            # 4 Actualizar la Vista
            self.vista.actualizar_vista_factura(self.modelo.factura_actual)

            # 5 Limpiar campos
            self.vista.combo_factura_articulo.set('')
            self.vista.entry_factura_cantidad.delete(0, 'end')
        
        except (ValueError, ArticuloNoEncontradoError, CantidadInvalidaError) as e:
            self.vista.mostrar_error("error al agregar linea", str(e))
    
    def eliminar_linea(self) -> None:
        """Maneja el clic en 'eliminar linea seleccionada'."""
        try:
            # 1 Validar que hay factura
            if not self.modelo.factura_actual:
                raise ValueError("no hay factura activa")

            # 2 Obtener seleccion del Treeview
            seleccion = self.vista.tree_factura_lineas.focus()
            if not seleccion:
                raise ValueError("debe seleccionar una linea")
            
            # Obtenemos el indice de la fila seleccionada
            indice = self.vista.tree_factura_lineas.index(seleccion)
            
            # 3 Llamar al Modelo
            self.modelo.eliminar_linea_factura(indice)
            
            # 4 Actualizar la Vista
            self.vista.actualizar_vista_factura(self.modelo.factura_actual)
        
        except ValueError as e:
            self.vista.mostrar_error("error al eliminar", str(e))

    #  Manejadores de eventos (Exportacion)

    def exportar_json(self) -> None:
        """Maneja el clic en 'exportar a json'."""
        try:
            if self.modelo.factura_actual:
                # 1 Llamar al Modelo
                self.modelo.exportar_factura_json()
                # 2 Mostrar info en la Vista
                self.vista.mostrar_info("exportacion", "factura exportada a json")
            else:
                raise ValueError("no hay factura para exportar")
        except Exception as e:
            self.vista.mostrar_error("error", str(e))

    def exportar_csv(self) -> None:
        """Maneja el clic en 'exportar a csv'."""
        try:
            if self.modelo.factura_actual:
                # 1Llamar al Modelo
                self.modelo.exportar_factura_csv()
                # 2 Mostrar info en la Vista
                self.vista.mostrar_info("exportacion", "factura exportada a csv")
            else:
                raise ValueError("no hay factura para exportar")
        except Exception as e:
            self.vista.mostrar_error("error", str(e))