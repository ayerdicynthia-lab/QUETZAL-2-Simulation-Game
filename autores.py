# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# ILUSTRACIONES: Cynthia Ayerdi, Natalia Sánchez
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Muestra los autores en una ventana toplevel
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA:
#   Fecha de creación: 1.7.26

from tkinter import Toplevel, Label
from formato import COLOR_FONDO_ACERCADE, COLOR_LETRA_ACERCADE
from formato import FONT_LETRA_ACERCADE

class Autores(Toplevel):
    def __init__(self)-> None:
        super().__init__()
        
        self.config(bg=COLOR_FONDO_ACERCADE)
        self.title("Acerca del programa")
        self.geometry("600x200")
        
        autor : str = "Autor: Cynthia Ayerdi"
        asesor : str = "Asesoría: Luis Carranza, Kuk Ho Chung"
        ilustraciones : str = "Ilustraciones: Cynthia Ayerdi, Natalia Sánchez"
        fecha : str = "Guatemala, xx de xx de 2026"
        lab : str = "Laboratorio Aeroespacial UVG"
        
        # Una lista del texto que va en la ventana para manipularlo mejor
        texto_ventana : list[str] = [
            autor,
            asesor,
            ilustraciones,
            fecha,
            lab
        ]
        
        for contenido in texto_ventana:
            Label(
                self,text=contenido, # va colocando el que corresponde en un label
                font=FONT_LETRA_ACERCADE,
                bg=COLOR_FONDO_ACERCADE,fg=COLOR_LETRA_ACERCADE
            ).pack(pady=2)
            
if __name__ == "__main__":
    Autores().mainloop()