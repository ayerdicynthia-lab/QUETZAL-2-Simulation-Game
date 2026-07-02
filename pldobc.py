# PLD-OBC OPERATION MODE le pasa el control a la Portenta hecha en casa
# El usuario (GCS) debe indicar cuánto tiempo se activará esto
# Permite probar PLD1 MILO y PLD2 LoRa

from tkinter import Toplevel, Label, Button
from tkinter import scrolledtext as st, Frame, messagebox as msg
from constantes import TICK, miliseg_a_seg
from formato import FONT_BOTON_PLDOBC, FONT_LETRA_PLDOBC, FONT_LETRITA_PLDOBC
from formato import COLOR_BOTON_PLDOBC, COLOR_FONDO_PLDOBC, COLOR_LETRA_PLDOBC
from formato import COLOR_LETRA_BOTON_PLDOBC, FONT_LETRITITA_PLD_OBC
from rutas_imagenes import SCHED_ANTENAS # CAMBIAR DESPUÉS A LAS OFICIALES
from rutas_imagenes import hacer_imagen

class PLD_OBC_VENTANA(Toplevel):
    def __init__(
        self,
        scheduler, #el master
        duracion_pldobc:int, # en milisegundos
        duracion_milo:int, # la suma de duracion de tomar fotos y verificarlas
        duracion_lora:int, # enviar datos a colegios
        prioridad_milo:int, #la mayor entre tomar y verificar fotos
        prioridad_lora:int
    )->None:
        super().__init__()
        
        self.geometry("670x650+20+20")
        self.resizable(False,False)
        self.title("PLD-OBC hecha en UVG")
        self.config(bg=COLOR_FONDO_PLDOBC)   
        
        # Un contenedor para centralizar los elementos en la pantalla
        contenedor = Frame(self,bg=COLOR_FONDO_PLDOBC)
        contenedor.pack(expand=True) 
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(1, weight=1)
        
        # Título
        Label(
            contenedor,
            text="MODO DE OPERACIÓN DE PLD-OBC",
            font=FONT_LETRA_PLDOBC,
            bg=COLOR_FONDO_PLDOBC,
            fg=COLOR_LETRA_PLDOBC
        ).grid(column=0,row=0,columnspan=2,pady=(2,1))
        
        #descripción
        Label(
            contenedor,
            text="Se ha transferido control a la computadora programada en UVG",
            font=FONT_LETRITA_PLDOBC,
            bg=COLOR_FONDO_PLDOBC,
            fg=COLOR_LETRA_PLDOBC
        ).grid(column=0,row=1,columnspan=2,pady=(1,2))
        
        # Imagen por ahora
        self.imagen = hacer_imagen(ruta=SCHED_ANTENAS,scaling=7.3)
        
        # para poner imágenes
        self.muestra_imagenes : Label = Label(
            contenedor,
            bg=COLOR_FONDO_PLDOBC,
            image=self.imagen, # La inicial
            height=250
        )
        self.muestra_imagenes.grid(column=0,row=2,columnspan=2,pady=(2,2))
        
        # Mostrar las tareas que se van ejecutando
        self.muestra_tareas = st.ScrolledText(
            contenedor,width=50,height=7,
            font=FONT_LETRITA_PLDOBC,
            fg=COLOR_LETRA_PLDOBC,
            state='disabled'
            )
        self.muestra_tareas.grid(column=0,row=3,columnspan=2)
        
        # Botones para ejecutar tareas de PLD1 y PLD2
        Label(
            contenedor,
            text=f"{" ENVIAR COMANDOS ":-^150}",
            bg=COLOR_FONDO_PLDOBC,
            fg=COLOR_LETRA_PLDOBC,
            font=FONT_LETRITA_PLDOBC
        ).grid(column=0,row=4,columnspan=2,pady=2)
        
        # Botones para enviar comandos
        self.boton_enviar = Button(
            contenedor,text="ENVIAR DATOS\nA COLEGIOS",
            fg=COLOR_LETRA_BOTON_PLDOBC,
            bg=COLOR_BOTON_PLDOBC,
            font=FONT_BOTON_PLDOBC,
            width=20,height=2
        )
        self.boton_enviar.grid(column=0,row=5,padx=4,pady=2)
        self.boton_fotos = Button(
            contenedor,text="TOMAR Y\n VERIFICAR FOTOS",
            fg=COLOR_LETRA_BOTON_PLDOBC,
            bg=COLOR_BOTON_PLDOBC,
            font=FONT_BOTON_PLDOBC,
            width=20,height=2
        )
        self.boton_fotos.grid(column=1,row=5,padx=4,pady=2)
        
        # Crédito ilustraciones
        Label(
            contenedor,
            text="Ilustraciones: Cynthia Ayerdi",
            bg=COLOR_FONDO_PLDOBC,
            fg=COLOR_LETRA_PLDOBC,
            font=FONT_LETRITITA_PLD_OBC
        ).place(x=50,y=313)
             
if __name__ == "__main__":
    ventana = PLD_OBC_VENTANA(
        scheduler=None, # no hay master acá
        duracion_pldobc=30_000, # milisegundos
        duracion_milo=6_000,
        duracion_lora=4_000,
        prioridad_lora=2,
        prioridad_milo=1
    )
    ventana.mainloop()