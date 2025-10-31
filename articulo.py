from abc import ABC, abstractmethod
from .excepciones import PrecioInvalidoError

class ArticuloBase(ABC):
    def __init__(self, codigo: str, denominacion: str, precio: float):
        self.__codigo = codigo
        self.__denominacion = denominacion
        self.precio = precio  # Usa el setter para la validacion

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def denominacion(self) -> str:
        return self.__denominacion

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float):
        """Valida que el precio no sea negativo"""
        if valor < 0:
            raise PrecioInvalidoError("el precio no puede ser negativo")
        self.__precio = valor
    
    @abstractmethod
    def calcular_precio_descuento(self) -> float:
        """Metodo abstracto para calcular el precio final (con descuentos)"""
        pass

class ArticuloFisico(ArticuloBase):
    """Articulo fisico que tiene un peso"""
    def __init__(self, codigo: str, denominacion: str, precio: float, peso: float):
        super().__init__(codigo, denominacion, precio)
        self.__peso = peso

    @property
    def peso(self) -> float:
        return self.__peso

    def calcular_precio_descuento(self) -> float:
        """Los articulos fisicos no tienen descuento"""
        return self.precio

class ArticuloDigital(ArticuloBase):
    """Articulo digital que tiene una licencia y descuento"""
    def __init__(self, codigo: str, denominacion: str, precio: float, licencia: str):
        super().__init__(codigo, denominacion, precio)
        self.__licencia = licencia

    @property
    def licencia(self) -> str:
        return self.__licencia
    
    def calcular_precio_descuento(self) -> float:
        """Los articulos digitales tienen un 10% de descuento"""
        return self.precio * 0.9