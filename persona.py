from abc import ABC, abstractmethod

class Persona(ABC):
    """
    Clase base abstracta para representar una persona
    No se pueden crear objetos de esta clase directamente
    """
    def __init__(self, nombre: str, apellidos: str):
        self.__nombre = nombre
        self.__apellidos = apellidos

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def apellidos(self) -> str:
        return self.__apellidos

    @abstractmethod
    def obtener_datos(self) -> str:
        """Metodo abstracto para obtener una representacion en string"""
        pass

class Cliente(Persona):
    """
    Clase que representa a un Cliente, hereda de Persona
    """
    def __init__(self, nombre: str, apellidos: str, dni: str):
        # Llamamos al constructor de la clase padre
        super().__init__(nombre, apellidos)
        self.__dni = dni

    @property
    def dni(self) -> str:
        return self.__dni

    def obtener_datos(self) -> str:
        """Implementacion del metodo abstracto"""
        return f"{self.nombre} {self.apellidos} ({self.dni})"