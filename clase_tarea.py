# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Clase tarea que solicita atributos relevantes para instanciar cada una de éstas,
# además tiene un método para "correrlas".
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA
#   Fecha de creación: 27.5.26
#       - Método para ejecutar (disminuir tiempo restante)
#       - Atributos: 
#           *prioridad
#           *id
#           *estado
#           *tiempo restante
#           *tiempo que lleva ejecutándose
#           *descripción
#   Modificaciones de UX: 28.5.26
#       - Se eliminó la propiedad de descripción para tener un id más claro y conciso,
#         con palabras menos "complicadas"
#       - Se muestra el tiempo en segundos
#   Atributo de imagen: 5.6.26
#       - También se recibe un label en donde se muestra esa imagen

from constantes import TICK, miliseg_a_seg
from PIL import ImageTk
from tkinter import Label

class Tarea():
    def __init__(self,
                 prioridad:int,
                 id:str,
                 estado:str,
                 tiempo_restante:int, # En milisegundos
                 tiempo_lleva:int, # En milisegundos
                 imagen:ImageTk.PhotoImage,
                 modo_operacion : str,
                 label_imagen:Label): 
        
        # Guardar los parámetros como variables de la clase para usarlos después
        self.prioridad = prioridad
        self.id = id
        self.estado = estado
        self.tiempo_restante = tiempo_restante
        self.tiempo_lleva = tiempo_lleva
        self.imagen=imagen
        self.label_imagen = label_imagen  
        self.modo_operacion = modo_operacion
        
    def ejecutar(self)->str:  
        
        # La ejecución sólo consiste en disminuir el tiempo restante
        self.tiempo_restante -= TICK
        
        # Y aumentar el tiempo que lleva ejecutándose
        self.tiempo_lleva += TICK 
        
        # Poner la imagen
        self.label_imagen.config(image=self.imagen)
        
        tiempo_lleva_segundos = miliseg_a_seg(self.tiempo_lleva) # Para que sea más intuitivo
        return f"{self.id} ha corrido por {tiempo_lleva_segundos}"
    
if __name__ == "__main__":
    print("Hola este archivo probablemente no es el que quieres correr JAJA")