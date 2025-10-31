"""
Excepciones personalizadas para un manejo de errores mas claro
"""

class CantidadInvalidaError(Exception):
    """Lanzada cuando la cantidad de un articulo es <= 0"""
    pass

class ArticuloNoEncontradoError(Exception):
    """Lanzada cuando no se encuentra un articulo por su codigo"""
    pass

class ClienteNoEncontradoError(Exception):
    """Lanzada cuando no se encuentra un cliente por su DNI"""
    pass

class PrecioInvalidoError(Exception):
    """Lanzada cuando se intenta poner un precio negativo"""
    pass