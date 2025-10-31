import json
import csv
from typing import List
from .interfaces import Exportable
from .excepciones import CantidadInvalidaError
from .persona import Cliente
from .articulo import ArticuloBase

class LineaFactura:
    """Representa una linea de la factura (Articulo + Cantidad)"""
    def __init__(self, articulo: ArticuloBase, cantidad: int):
        if cantidad <= 0:
            raise CantidadInvalidaError("la cantidad debe ser positiva")
        self.__articulo = articulo
        self.__cantidad = cantidad

    @property
    def articulo(self) -> ArticuloBase:
        return self.__articulo

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def subtotal(self) -> float:
        """Propiedad calculada para el subtotal"""
        return self.articulo.calcular_precio_descuento() * self.cantidad

class Factura(Exportable):
    """
    Representa una factura completa, asociada a un cliente
    Implementa la interfaz Exportable
    """
    def __init__(self, cliente: Cliente):
        self.__cliente = cliente
        self.__lineas: List[LineaFactura] = []
        self.__total = 0.0

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def lineas(self) -> List[LineaFactura]:
        return self.__lineas

    @property
    def total(self) -> float:
        """Propiedad calculada para el total"""
        self.calcular_total()
        return self.__total

    def agregar_linea(self, articulo: ArticuloBase, cantidad: int) -> None:
        """Añade una nueva linea a la factura."""
        linea = LineaFactura(articulo, cantidad)
        self.__lineas.append(linea)
        self.calcular_total() # Recalcula el total

    def eliminar_linea(self, indice: int) -> None:
        """Elimina una linea por su indice."""
        if 0 <= indice < len(self.__lineas):
            del self.__lineas[indice]
            self.calcular_total() # Recalcula el total

    def calcular_total(self) -> None:
        """Metodo privado para recalcular el total de la factura"""
        self.__total = sum(linea.subtotal for linea in self.__lineas)

    def exportar_json(self) -> None:
        """Exporta la factura a un archivo JSON"""
        datos = {
            "cliente": self.cliente.obtener_datos(),
            "total": self.total,
            "lineas": [
                {
                    "articulo": linea.articulo.denominacion,
                    "cantidad": linea.cantidad,
                    "subtotal": linea.subtotal
                } for linea in self.lineas
            ]
        }
        # Guardamos el archivo
        with open(f"factura_{self.cliente.dni}.json", "w") as f:
            json.dump(datos, f, indent=4)
        print("factura exportada a json")

    def exportar_csv(self) -> None:
        """Exporta la factura a un archivo CSV"""
        with open(f"factura_{self.cliente.dni}.csv", "w", newline='') as f:
            writer = csv.writer(f)
            # Escribimos los datos del cliente y total
            writer.writerow(["Cliente", self.cliente.obtener_datos()])
            writer.writerow(["Total", self.total])
            writer.writerow([]) # Linea en blanco
            # Escribimos las cabeceras de las lineas
            writer.writerow(["Articulo", "Cantidad", "Subtotal"])
            # Escribimos cada linea
            for linea in self.lineas:
                writer.writerow([
                    linea.articulo.denominacion,
                    linea.cantidad,
                    linea.subtotal
                ])
        print("factura exportada a csv")