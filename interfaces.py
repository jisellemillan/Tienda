from abc import ABC, abstractmethod

class Exportable(ABC):
    """
    Interfaz abstracta para clases que pueden ser exportadas
    Define los metodos que las subclases DEBEN implementar
    """
    
    @abstractmethod
    def exportar_json(self) -> None:
        """Exporta los datos a un archivo JSON"""
        pass

    @abstractmethod
    def exportar_csv(self) -> None:
        """Exporta los datos a un archivo CSV"""
        pass