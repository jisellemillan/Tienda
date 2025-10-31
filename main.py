import tkinter as tk
from vista.vista_tk import VistaPrincipal
from controlador.controlador import Controlador
from modelo.modelo_logica import ModeloLogica

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicacion
    Crea la raiz de tkinter y las tres partes de MVC
    """
    
    # 1 Crear la ventana principal
    root = tk.Tk()
    
    # 2 Crear las instancias de M-V-C
    modelo = ModeloLogica()
    vista = VistaPrincipal(root)
    controlador = Controlador(modelo, vista) # Conecta el modelo y la vista
    
    # 3 Iniciar el bucle de la aplicacion
    root.mainloop()