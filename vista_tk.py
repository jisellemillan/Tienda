import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from modelo.persona import Cliente
from modelo.articulo import ArticuloBase
from modelo.factura import Factura

class VistaPrincipal:
    """
    Contiene todos los widgets de Tkinter (ttk)
    NO contiene logica de negocio, solo dibuja la pantalla
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("sistema de facturacion")
        self.root.geometry("800x600")

        # Crear el sistema de pestañas (Notebook)
        self.notebook = ttk.Notebook(root)
        
        # Pestaña 1: Clientes
        self.tab_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clientes, text='clientes')
        self.crear_tab_clientes()

        # Pestaña 2: Articulos
        self.tab_articulos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_articulos, text='articulos')
        self.crear_tab_articulos()

        # Pestaña 3: Facturacion
        self.tab_facturacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_facturacion, text='facturacion')
        self.crear_tab_facturacion()

        self.notebook.pack(expand=1, fill='both')
    
    #  Metodos publicos (para el Controlador) 
    
    def mostrar_error(self, titulo: str, mensaje: str) -> None:
        """Muestra una ventana emergente de error."""
        messagebox.showerror(titulo, mensaje)

    def mostrar_info(self, titulo: str, mensaje: str) -> None:
        """Muestra una ventana emergente de informacion."""
        messagebox.showinfo(titulo, mensaje)

    def crear_tab_clientes(self) -> None:
        """Dibuja todos los widgets de la pestaña Clientes."""
        
        # Formulario de registro
        frame_form = ttk.LabelFrame(self.tab_clientes, text="registrar cliente")
        frame_form.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_form, text="nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_cliente_nombre = ttk.Entry(frame_form)
        self.entry_cliente_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="apellidos:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cliente_apellidos = ttk.Entry(frame_form)
        self.entry_cliente_apellidos.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="dni:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_cliente_dni = ttk.Entry(frame_form)
        self.entry_cliente_dni.grid(row=2, column=1, padx=5, pady=5)

        self.btn_registrar_cliente = ttk.Button(frame_form, text="registrar")
        self.btn_registrar_cliente.grid(row=3, column=0, columnspan=2, pady=10)

        # Lista (Treeview) de clientes
        frame_lista = ttk.LabelFrame(self.tab_clientes, text="lista de clientes")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_clientes = ttk.Treeview(frame_lista, columns=("nombre", "apellidos", "dni"), show="headings")
        self.tree_clientes.heading("nombre", text="nombre")
        self.tree_clientes.heading("apellidos", text="apellidos")
        self.tree_clientes.heading("dni", text="dni")
        self.tree_clientes.pack(fill="both", expand=True)

        self.btn_eliminar_cliente = ttk.Button(frame_lista, text="eliminar seleccionado")
        self.btn_eliminar_cliente.pack(pady=5)

    def actualizar_lista_clientes(self, clientes: List[Cliente]) -> None:
        """Limpia y rellena la tabla de clientes con datos nuevos"""
        # Limpiar tabla
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        # Rellenar
        for cliente in clientes:
            self.tree_clientes.insert("", "end", values=(cliente.nombre, cliente.apellidos, cliente.dni))

    def crear_tab_articulos(self) -> None:
        """Dibuja todos los widgets de la pestaña Articulos"""
        frame_form = ttk.LabelFrame(self.tab_articulos, text="registrar articulo")
        frame_form.pack(fill="x", padx=10, pady=10)

        # Radio buttons para tipo
        ttk.Label(frame_form, text="tipo:").grid(row=0, column=0, padx=5, pady=5)
        self.tipo_articulo_var = tk.StringVar(value="fisico")
        ttk.Radiobutton(frame_form, text="fisico", variable=self.tipo_articulo_var, value="fisico", command=self.actualizar_form_articulo).grid(row=0, column=1)
        ttk.Radiobutton(frame_form, text="digital", variable=self.tipo_articulo_var, value="digital", command=self.actualizar_form_articulo).grid(row=0, column=2)

        # Campos comunes
        ttk.Label(frame_form, text="codigo:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_articulo_codigo = ttk.Entry(frame_form)
        self.entry_articulo_codigo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="denominacion:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_articulo_denominacion = ttk.Entry(frame_form)
        self.entry_articulo_denominacion.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="precio:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_articulo_precio = ttk.Entry(frame_form)
        self.entry_articulo_precio.grid(row=3, column=1, padx=5, pady=5)

        # Campo extra (depende del tipo)
        self.label_articulo_extra = ttk.Label(frame_form, text="peso:")
        self.label_articulo_extra.grid(row=4, column=0, padx=5, pady=5)
        self.entry_articulo_extra = ttk.Entry(frame_form)
        self.entry_articulo_extra.grid(row=4, column=1, padx=5, pady=5)

        self.btn_registrar_articulo = ttk.Button(frame_form, text="registrar")
        self.btn_registrar_articulo.grid(row=5, column=0, columnspan=2, pady=10)

        # Lista (Treeview) de articulos
        frame_lista = ttk.LabelFrame(self.tab_articulos, text="lista de articulos")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_articulos = ttk.Treeview(frame_lista, columns=("codigo", "denominacion", "precio", "tipo"), show="headings")
        self.tree_articulos.heading("codigo", text="codigo")
        self.tree_articulos.heading("denominacion", text="denominacion")
        self.tree_articulos.heading("precio", text="precio")
        self.tree_articulos.heading("tipo", text="tipo")
        self.tree_articulos.pack(fill="both", expand=True)

    def actualizar_form_articulo(self) -> None:
        """Cambia la etiqueta del campo 'extra' (peso/licencia)."""
        tipo = self.tipo_articulo_var.get()
        if tipo == "fisico":
            self.label_articulo_extra.config(text="peso:")
        else:
            self.label_articulo_extra.config(text="licencia:")

    def actualizar_lista_articulos(self, articulos: List[ArticuloBase]) -> None:
        """Limpia y rellena la tabla de articulos"""
        self.tree_articulos.delete(*self.tree_articulos.get_children())
        for articulo in articulos:
            # Determinamos el tipo para mostrar en la tabla
            tipo = "fisico" if hasattr(articulo, "peso") else "digital"
            self.tree_articulos.insert("", "end", values=(articulo.codigo, articulo.denominacion, articulo.precio, tipo))

    def crear_tab_facturacion(self) -> None:
        """Dibuja todos los widgets de la pestaña Facturacion"""
        
        # Frame para crear nueva factura
        frame_seleccion = ttk.Frame(self.tab_facturacion)
        frame_seleccion.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_seleccion, text="seleccionar cliente (dni):").pack(side=tk.LEFT, padx=5)
        self.combo_factura_cliente = ttk.Combobox(frame_seleccion)
        self.combo_factura_cliente.pack(side=tk.LEFT, padx=5)
        self.btn_nueva_factura = ttk.Button(frame_seleccion, text="nueva factura")
        self.btn_nueva_factura.pack(side=tk.LEFT, padx=5)

        # Frame principal de la factura
        frame_factura = ttk.LabelFrame(self.tab_facturacion, text="factura actual")
        frame_factura.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.label_cliente_factura = ttk.Label(frame_factura, text="cliente: (ninguno)")
        self.label_cliente_factura.pack(anchor="w", padx=5, pady=5)

        # Frame para agregar lineas
        frame_agregar_linea = ttk.Frame(frame_factura)
        frame_agregar_linea.pack(fill="x", pady=5)
        
        ttk.Label(frame_agregar_linea, text="articulo (codigo):").pack(side=tk.LEFT, padx=5)
        self.combo_factura_articulo = ttk.Combobox(frame_agregar_linea)
        self.combo_factura_articulo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_agregar_linea, text="cantidad:").pack(side=tk.LEFT, padx=5)
        self.entry_factura_cantidad = ttk.Entry(frame_agregar_linea, width=5)
        self.entry_factura_cantidad.pack(side=tk.LEFT, padx=5)
        
        self.btn_agregar_linea = ttk.Button(frame_agregar_linea, text="agregar linea")
        self.btn_agregar_linea.pack(side=tk.LEFT, padx=5)

        # Lista (Treeview) de lineas de factura
        self.tree_factura_lineas = ttk.Treeview(frame_factura, columns=("articulo", "cantidad", "subtotal"), show="headings")
        self.tree_factura_lineas.heading("articulo", text="articulo")
        self.tree_factura_lineas.heading("cantidad", text="cantidad")
        self.tree_factura_lineas.heading("subtotal", text="subtotal")
        self.tree_factura_lineas.pack(fill="both", expand=True, pady=5)
        
        self.btn_eliminar_linea = ttk.Button(frame_factura, text="eliminar linea seleccionada")
        self.btn_eliminar_linea.pack(pady=5)

        # Total y botones de exportacion
        self.label_factura_total = ttk.Label(frame_factura, text="total: $0.00", font=("Arial", 14, "bold"))
        self.label_factura_total.pack(anchor="e", padx=10, pady=10)

        frame_exportar = ttk.Frame(frame_factura)
        frame_exportar.pack(fill="x", pady=10)
        self.btn_exportar_json = ttk.Button(frame_exportar, text="exportar a json")
        self.btn_exportar_json.pack(side=tk.RIGHT, padx=5)
        self.btn_exportar_csv = ttk.Button(frame_exportar, text="exportar a csv")
        self.btn_exportar_csv.pack(side=tk.RIGHT, padx=5)

    def actualizar_combos(self, clientes: List[Cliente], articulos: List[ArticuloBase]) -> None:
        """Actualiza los desplegables (Combobox) con clientes y articulos"""
        self.combo_factura_cliente['values'] = [c.dni for c in clientes]
        self.combo_factura_articulo['values'] = [a.codigo for a in articulos]
    
    def actualizar_vista_factura(self, factura: Optional[Factura]) -> None:
        """Actualiza toda la pestaña de factura con los datos de la factura activa"""
        # Limpiar tabla
        self.tree_factura_lineas.delete(*self.tree_factura_lineas.get_children())
        
        if factura:
            # Si hay factura, rellenamos todo
            self.label_cliente_factura.config(text=f"cliente: {factura.cliente.obtener_datos()}")
            for linea in factura.lineas:
                self.tree_factura_lineas.insert("", "end", values=(linea.articulo.denominacion, linea.cantidad, f"{linea.subtotal:.2f}"))
            self.label_factura_total.config(text=f"total: ${factura.total:.2f}")
        else:
            # Si no hay factura, reseteamos las etiquetas
            self.label_cliente_factura.config(text="cliente: (ninguno)")
            self.label_factura_total.config(text="total: $0.00")