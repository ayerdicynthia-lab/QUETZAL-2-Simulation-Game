# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# ILUSTRACIONES: Cynthia Ayerdi, Natalia Sánchez
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Permite que el usuario seleccione la duración y la prioridad de cada una de las
# tareas que realiza la simulación.
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA:
#   Fecha de creación: 27.5.26
#       - Permite seleccionar prioridad en un spinbox con valores entre 1 y 5
#       - Tarea captura imágenes y tarea recolección datos
#   Mejoras de UX: 28.5.26
#       - Elimina la descripción
#       - Cambia los IDs a definiciones más claras de la tarea
#       - permite que el usuario ingrese el tiempo que quiere que dure cada tarea
#   Acerca de: 3.6.26
#   Imágenes: 5.6.26
#       - Imágenes ilustrativas en el seleccionador
#       - Ya no se pasan las tareas al scheduler, sólo la prioridad y la duración. Para que 
#         las imágenes si sean un atributo de la clase
#   Modificación acerca de: 1.7.26
#       - Mostrarlo como una ventana Toplevel

from tkinter import Tk, Button, Label, Spinbox, Frame, IntVar, messagebox as msg
from constantes import COLOR_FONDO_SELECT,COLOR_LETRA_SELECT
from constantes import COLOR_LETRA_BOTON,COLOR_BOTON
from constantes import FONT_LETRA_SELECT,FONT_LETRITA_SELECT,COLOR_LETRITA_SELECT
from constantes import SELECT_ANTENAS, SELECT_SIMPLE, SELECT_DEORBIT
from constantes import hacer_imagen
from scheduler import Scheduler_Ventana
from autores import Autores

class Seleccionador(Tk): 
    # Interfaz en donde el usuario selecciona qué prioridad darle a cada tarea
    
    def __init__(self)->None:
        super().__init__()
        self.geometry("950x520+20+20")
        self.resizable(False,False)
        self.config(background=COLOR_FONDO_SELECT)
        self.title("Selecciona")
        
        # Un contenedor para centralizar los elementos en la pantalla
        contenedor = Frame(self,bg=COLOR_FONDO_SELECT)
        contenedor.pack(expand=True) 
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(1, weight=1)
        contenedor.grid_columnconfigure(2, weight=1)
        
        # Recolección de datos
        Label(
            contenedor,
            text="Tarea RECOLECCIÓN DE DATOS",
            font = FONT_LETRA_SELECT,
            fg=COLOR_LETRA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=0,column=0,columnspan=2,padx=5,pady=5
        )   
        # Prioridad
        Label(
            contenedor,
            text=f"Seleccione PRIORIDAD:",
            font = FONT_LETRITA_SELECT,
            fg=COLOR_LETRITA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=1,column=0,padx=5,pady=5,sticky="E"
        )      
        self.ingreso_prioridad_recoleccion_datos = Spinbox(
            contenedor,from_=1,to=5,width=8,
            textvariable=IntVar(value=1), #La opción predeterminada
            font=FONT_LETRITA_SELECT,
            justify="center",
            fg=COLOR_LETRA_SELECT,
            state="readonly" # No permite que el usuario ingrese sus propios valores
        ) 
        self.ingreso_prioridad_recoleccion_datos.grid(row=1,column=1,padx=5,pady=5,sticky='W') 
        # Duración
        Label(
            contenedor,
            text=f"Seleccione DURACIÓN:",
            font = FONT_LETRITA_SELECT,
            fg=COLOR_LETRITA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=2,column=0,padx=5,pady=5,sticky="E"
        )      
        self.ingreso_duracion_recoleccion_datos = Spinbox(
            contenedor,from_=1,to=10,width=8,
            textvariable=IntVar(value=8), #La opción predeterminada
            font=FONT_LETRITA_SELECT,
            justify="center",
            fg=COLOR_LETRA_SELECT,
            state="readonly" # No permite que el usuario ingrese sus propios valores
        ) 
        self.ingreso_duracion_recoleccion_datos.grid(row=2,column=1,padx=5,pady=5,sticky='W')
        
        # Para la captura de imágenes ("sólo sobre Guatemala")
        Label(
            contenedor,
            text=f"Tarea TOMAR FOTOS",
            font = FONT_LETRA_SELECT,
            fg=COLOR_LETRA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=3,columnspan=2,column=0,padx=5,pady=5
        )      
        #Prioridad
        Label(
            contenedor,
            text=f"Seleccione PRIORIDAD:",
            font = FONT_LETRITA_SELECT,
            fg=COLOR_LETRITA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=4,column=0,padx=5,pady=5,sticky="E"
        )    
        self.ingreso_prioridad_captura_imagenes = Spinbox(
            contenedor,from_=1,to=5,width=8,
            textvariable=IntVar(value=3), #La opción predeterminada
            font=FONT_LETRITA_SELECT,
            justify="center",
            fg=COLOR_LETRA_SELECT,
            state="readonly"
        ) 
        self.ingreso_prioridad_captura_imagenes.grid(row=4,column=1,padx=5,pady=5,sticky='W')
        # Duración
        Label(
            contenedor,
            text=f"Seleccione DURACIÓN:",
            font = FONT_LETRITA_SELECT,
            fg=COLOR_LETRITA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=5,column=0,padx=5,pady=5,sticky="E"
        )      
        self.ingreso_duracion_captura_imagenes = Spinbox(
            contenedor,from_=1,to=10,width=8,
            textvariable=IntVar(value=4), #La opción predeterminada
            font=FONT_LETRITA_SELECT,
            justify="center",
            fg=COLOR_LETRA_SELECT,
            state="readonly" # No permite que el usuario ingrese sus propios valores
        ) 
        self.ingreso_duracion_captura_imagenes.grid(row=5,column=1,padx=5,pady=5,sticky='W')
        
        # Para verificar si las imágenes tienen nubes
        Label(
            contenedor,
            text=f"Tarea VERIFICAR FOTOS",
            font=FONT_LETRA_SELECT,
            fg=COLOR_LETRA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=6,column=0,columnspan=2,padx=5,pady=5
        )      
        #Prioridad
        Label(
            contenedor,
            text=f"Seleccione PRIORIDAD:",
            font = FONT_LETRITA_SELECT,
            fg=COLOR_LETRITA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=7,column=0,padx=5,pady=5,sticky="E"
        )    
        self.ingreso_prioridad_verifica_imagenes = Spinbox(
            contenedor,from_=1,to=5,width=8,
            textvariable=IntVar(value=2), #La opción predeterminada
            font=FONT_LETRITA_SELECT,
            justify="center",
            fg=COLOR_LETRA_SELECT,
            state="readonly"
        ) 
        self.ingreso_prioridad_verifica_imagenes.grid(row=7,column=1,padx=5,pady=5,sticky='W')
        # Duración
        Label(
            contenedor,
            text=f"Seleccione DURACIÓN:",
            font = FONT_LETRITA_SELECT,
            fg=COLOR_LETRITA_SELECT,
            background=COLOR_FONDO_SELECT
        ).grid(
            row=8,column=0,padx=5,pady=5,sticky="E"
        )      
        self.ingreso_duracion_verifica_imagenes = Spinbox(
            contenedor,from_=1,to=10,width=8,
            textvariable=IntVar(value=5), #La opción predeterminada
            font=FONT_LETRITA_SELECT,
            justify="center",
            fg=COLOR_LETRA_SELECT,
            state="readonly" # No permite que el usuario ingrese sus propios valores
        ) 
        self.ingreso_duracion_verifica_imagenes.grid(row=8,column=1,padx=5,pady=5,sticky='W')
        
        Button(
            contenedor,text="Enviar Tareas al Scheduler",
            fg=COLOR_LETRA_BOTON,bg=COLOR_BOTON,font=FONT_LETRITA_SELECT,
            command=self.enviar_informacion_al_scheduler
        ).grid(row=9,column=0,columnspan=2,padx=5,pady=5)
        Button(
            contenedor,text="Acerca del Programa",
            fg=COLOR_LETRA_BOTON,bg=COLOR_BOTON,font=FONT_LETRITA_SELECT,
            command=self.acerca_de
        ).grid(row=10,column=0,columnspan=2,padx=5,pady=5)
        
        # - - - ILUSTRACIONES - - -
        self.satelite_simpleselect = hacer_imagen(SELECT_SIMPLE,scaling=2)
        self.satelite_antenasselect = hacer_imagen(SELECT_ANTENAS,scaling=2)
        self.deorbitselect = hacer_imagen(SELECT_DEORBIT,scaling=2)
        
        # Labels para poner imágenes
        Label(
            self,
            bg=COLOR_FONDO_SELECT,
            image=self.satelite_simpleselect
        ).place(x=45,y=40)
        Label(
            self,
            bg=COLOR_FONDO_SELECT,
            image=self.satelite_antenasselect
        ).place(x=700,y=110)
        Label(
            self,
            bg=COLOR_FONDO_SELECT,
            image=self.deorbitselect
        ).place(x=50,y=260)
        
    def acerca_de(self):
        ventana_acercade = Autores()
        ventana_acercade.mainloop()
    
    def enviar_informacion_al_scheduler(self)->None:
        # Obtener las prioridades y duraciones ingresadas por el usuario
        # Instanciar las tareas correspondientes con esos valores y enviarlas al scheduler
        
        # En el spinbox sólo se pueden seleccionar los enteros ahí colocados
        # No es necesario validar este ingreso
        prioridad_recoleccion_datos : int= int(self.ingreso_prioridad_recoleccion_datos.get()) 
        prioridad_captura_imagenes : int = int(self.ingreso_prioridad_captura_imagenes.get())
        prioridad_verifica_imagenes : int = int(self.ingreso_prioridad_verifica_imagenes.get())
        
        # El ingreso es en segundos, por lo que se debe pasar a milisegundos
        # multiplicando el valor ingresado por 1000
        duracion_recoleccion_datos = int(self.ingreso_duracion_recoleccion_datos.get())*1000
        duracion_captura_imagenes = int(self.ingreso_duracion_captura_imagenes.get())*1000
        duracion_verifica_imagenes = int(self.ingreso_duracion_verifica_imagenes.get())*1000
              
        # Para que el usuario pueda verificar lo que ingresó antes de continuar
        confirmacionT1 : str = f"Recolectar datos: Prioridad {prioridad_recoleccion_datos}. Duración {duracion_recoleccion_datos//1000} segundos."
        confirmacionT2 : str = f"Tomar fotos: Prioridad {prioridad_captura_imagenes}. Duración {duracion_captura_imagenes//1000} segundos."
        confirmacionT3 : str = f"Verificar fotos: Prioridad {prioridad_verifica_imagenes}. Duración {duracion_verifica_imagenes//1000} segundos."
        
        mensaje : str = f"{confirmacionT1}\n{confirmacionT2}\n{confirmacionT3}"
        if msg.askyesno("¿Desea continuar?",mensaje):
        
            self.destroy()
            # Instancia un objeto scheduler con la información de las tareas
            scheduler = Scheduler_Ventana(
                prioridad_capturar=prioridad_captura_imagenes,
                duracion_capturar=duracion_captura_imagenes,
                prioridad_verificar=prioridad_verifica_imagenes,
                duracion_verificar=duracion_verifica_imagenes,
                prioridad_recoleccion=prioridad_recoleccion_datos,
                duracion_recoleccion=duracion_recoleccion_datos
            ) 
        
             # Quitar la ventanita del seleccionador
            scheduler.mainloop()
        
if __name__ == "__main__":
    Seleccionador().mainloop()