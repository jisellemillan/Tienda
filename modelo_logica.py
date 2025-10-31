from typing import List, Optional
from .persona import Cliente
from .articulo import ArticuloBase, ArticuloFisico, ArticuloDigital
from .factura import Factura
from .excepciones import ClienteNoEncontradoError, ArticuloNoEncontradoError

class ModeloLogica:
    """
    Maneja toda la logica de negocio y los datos (listas).
    Es la unica clase con la que hablara el Controlador.
    """
    def __init__(self):
        self.__clientes: List[Cliente] = []
        self.__articulos: List[ArticuloBase] = []
        self.__factura_actual: Optional[Factura] = None

    # Propiedades 
    
    @property
    def clientes(self) -> List[Cliente]:
        return self.__clientes

    @property
    def articulos(self) -> List[ArticuloBase]:
        return self.__articulos

    @property
    def factura_actual(self) -> Optional[Factura]:
        return self.__factura_actual

    #  Metodos Clientes

    def registrar_cliente(self, nombre: str, apellidos: str, dni: str) -> Cliente:
        """Crea y guarda un nuevo cliente"""
        cliente = Cliente(nombre, apellidos, dni)
        self.__clientes.append(cliente)
        return cliente

    def eliminar_cliente(self, dni: str) -> None:
        """Elimina un cliente de la lista usando su DNI"""
        cliente = self.buscar_cliente(dni) # Reusa el metodo buscar
        self.__clientes.remove(cliente)

    def buscar_cliente(self, dni: str) -> Cliente:
        """Busca un cliente por DNI Lanza error si no lo encuentra"""
        for cliente in self.__clientes:
            if cliente.dni == dni:
                return cliente
        raise ClienteNoEncontradoError("cliente no encontrado")

    #  Metodos Articuloz
    
    def registrar_articulo_fisico(self, codigo: str, denominacion: str, precio: float, peso: float) -> ArticuloFisico:
        """Crea y guarda un nuevo articulo fisico"""
        articulo = ArticuloFisico(codigo, denominacion, precio, peso)
        self.__articulos.append(articulo)
        return articulo
    
    def registrar_articulo_digital(self, codigo: str, denominacion: str, precio: float, licencia: str) -> ArticuloDigital:
        """Crea y guarda un nuevo articulo digital"""
        articulo = ArticuloDigital(codigo, denominacion, precio, licencia)
        self.__articulos.append(articulo)
        return articulo

    def buscar_articulo(self, codigo: str) -> ArticuloBase:
        """Busca un articulo por codigo. Lanza error si no lo encuentra"""
        for articulo in self.__articulos:
            if articulo.codigo == codigo:
                return articulo
        raise ArticuloNoEncontradoError("articulo no encontrado")

    # Metodos Factura 

    def crear_nueva_factura(self, dni_cliente: str) -> Factura:
        """Inicia una nueva factura para un cliente"""
        cliente = self.buscar_cliente(dni_cliente)
        self.__factura_actual = Factura(cliente)
        return self.__factura_actual

    def agregar_linea_factura(self, codigo_articulo: str, cantidad: int) -> None:
        """Agrega una linea a la factura actual"""
        if self.__factura_actual:
            articulo = self.buscar_articulo(codigo_articulo)
            self.__factura_actual.agregar_linea(articulo, cantidad)
    
    def eliminar_linea_factura(self, indice: int) -> None:
        """Elimina una linea de la factura actual por su indice"""
        if self.__factura_actual:
            self.__factura_actual.eliminar_linea(indice)

    def exportar_factura_json(self) -> None:
        """Exporta la factura actual a JSON"""
        if self.__factura_actual:
            self.__factura_actual.exportar_json()
    
    def exportar_factura_csv(self) -> None:
        """Exporta la factura actual a CSV"""
        if self.__factura_actual:
            self.__factura_actual.exportar_csv()