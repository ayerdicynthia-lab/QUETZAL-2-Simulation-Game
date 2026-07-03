# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# ILUSTRACIONES: Cynthia Ayerdi
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Scheduler basado en un Sistema Operativo en Tiempo Real usando prioridades 
# y tiempos de ejecución. El usuario puede enviar alguno de cuatro comandos, cada uno con una 
# prioridad, para observar el funcionamiento de preemption y round-robin. Además, se incorporan
# los modos de operación de emergencia relacionados con la computadora principal y el mecanismo
# de deorbit.
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA:
#   Fecha de creación: 2.7.26
#   - interfaz de usuario
#   Funcionalidad: 3.7.26
#   - Su propio scheduler con preemption (no round-robin)

from tkinter import Toplevel, Label, Button
from tkinter import scrolledtext as st, Frame, messagebox as msg
from constantes import TICK, miliseg_a_seg
from formato import FONT_BOTON_PLDOBC, FONT_LETRA_PLDOBC, FONT_LETRITA_PLDOBC
from formato import COLOR_BOTON_PLDOBC, COLOR_FONDO_PLDOBC, COLOR_LETRA_PLDOBC
from formato import COLOR_LETRA_BOTON_PLDOBC, FONT_LETRITITA_PLD_OBC
from rutas_imagenes import SCHED_ANTENAS # CAMBIAR DESPUÉS A LAS OFICIALES
from rutas_imagenes import hacer_imagen
from clase_tarea import Tarea

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
        super().__init__(scheduler)
        
        self.scheduler = scheduler
        self.tiempo_maximo = duracion_pldobc # para que no se pase
        self.tiempo_corriendo = 0 # inicializando para ir sumando en cada tick
        
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
            contenedor,width=55,height=7,
            font=FONT_LETRITA_PLDOBC,
            fg=COLOR_LETRA_PLDOBC,
            state='disabled'
            )
        self.muestra_tareas.grid(column=0,row=3,columnspan=2)
        
        # Botones para ejecutar tareas de PLD1 y PLD2
        Label(
            contenedor,
            text=f'{" ENVIAR COMANDOS " :-^150}',
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
            width=20,height=2,
            command=self.comando_enviar_datos
        )
        self.boton_enviar.grid(column=0,row=5,padx=4,pady=2)
        self.boton_fotos = Button(
            contenedor,text="TOMAR Y\n VERIFICAR FOTOS",
            fg=COLOR_LETRA_BOTON_PLDOBC,
            bg=COLOR_BOTON_PLDOBC,
            font=FONT_BOTON_PLDOBC,
            width=20,height=2,
            command=self.comando_fotos
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
        
        # guardar para usar después
        self.prioridad_milo = prioridad_milo
        self.duracion_milo = duracion_milo
        self.prioridad_lora = prioridad_lora
        self.duracion_lora = duracion_lora
        
        # Definicion de tareas
        self.tMILO = Tarea(
            prioridad=self.prioridad_milo,
            id="Tomar y verificar fotos de Guatemala",
            estado="Blocked",
            tiempo_restante=self.duracion_milo,
            tiempo_lleva=0,
            imagen=self.imagen, #por ahora, cambiar después
            modo_operacion="a", # no es relevante porque todo esto es pld-obc operation mode
            label_imagen=self.muestra_imagenes
        )
        self.tLORA = Tarea(
            prioridad=self.prioridad_lora,
            id="Enviar datos del satélite a colegios",
            estado="Blocked",
            tiempo_restante=self.duracion_lora,
            tiempo_lleva=0,
            imagen=self.imagen, #por ahora, cambiar después
            modo_operacion="a", # no es relevante porque todo esto es pld-obc operation mode
            label_imagen=self.muestra_imagenes
        )
        self.tIDLE = Tarea(
            prioridad=0,
            id="Verificando PLD-OBC",
            estado="Running",
            tiempo_restante=1_000_000,
            tiempo_lleva=0,
            imagen=self.imagen, #por ahora, cambiar después
            modo_operacion="a", # no es relevante porque todo esto es pld-obc operation mode
            label_imagen=self.muestra_imagenes
        )
        
        # variables para el manejo del programa
        self.cerrar_ventana = False # para ver si en la próxima vuelta se cerrará
        
        # Lista de todas las tareas que hay para hacer
        self.tareas = [self.tLORA,self.tMILO,self.tIDLE]
        self.tarea_actual = self.tIDLE # empieza con la de espera
        
        self.after(TICK,self.tick_tick_tick)
    
    def meter_mensaje(self,mensaje:str,donde:st.ScrolledText)->None:
        # Para colocar el mensaje en el historial
        
        donde.config(state="normal")
        donde.insert("end",f"{mensaje}\n")
        donde.config(state="disabled")
        donde.see("end") # Baja al final del texto
        
    def comandan(self,tarea:Tarea,tiempo:int)-> None:
        # Función que actualiza el estado de la tarea cuando se manda a hacer
        # Para que esté ready y se pueda ejecutar según prioridad
        
        tarea.estado = "Ready"
        tarea.tiempo_restante = tiempo # El tiempo que se debe tardar según lo inicializado
        tarea.tiempo_lleva = 0
        
    def comando_enviar_datos(self)->None: 
        self.comandan(tarea=self.tLORA,tiempo=self.duracion_lora)
        
    def comando_fotos(self)->None:
        self.comandan(tarea=self.tMILO,tiempo=self.duracion_milo)
        
    def buscar_cuales_estan_listas(self)->list[Tarea]:
        # De la lista de tareas encuentra cuáles están en un estado ready o running
        # Y las devuelve en una lista
        
        tareitas_listas : list[Tarea] = [] # Inicializar la lista de tareas que están listas
        for tarea in self.tareas:
            
            if tarea.estado == "Ready" or tarea.estado=="Running":
                # Agrega sólo las tareas ready o running 
                # a la lista de tareas ready o running.
                tareitas_listas.append(tarea) 
                
        return tareitas_listas 
    
    def cual_tiene_mayor_prioridad(self,tareas_listas:list[Tarea])->Tarea|None:
        # Devuelve la tarea lista con mayor prioridad
        
        # Si no hay tareas listas, ni hay que meterse a ver cuál tiene más prioridad
        # Porque no hay nada
        if len(tareas_listas)==0:
            return None
        
        # inicializar
        candidata = tareas_listas[0]
        mayor_prioridad = candidata.prioridad #asumir que la primera tiene mayor prioridad 
        
        for tarea in tareas_listas:
            if tarea.prioridad > mayor_prioridad: # la bota
                candidata = tarea # la mayor por ahora
                mayor_prioridad = tarea.prioridad # competirán con esa prioridad
                
        return candidata   
    
    def ya_finalizo(self,tarea:Tarea)->bool:
        # Verifica si una tarea ha finalizado
        # Comprueba si ya no hay tiempo restante de ejecución
        
        if tarea.tiempo_restante <= 0: # Ya no queda nada "por hacer"
            tarea.estado = "Blocked"
            return True # Se acabó
        
        return False # Si aún hay tiempo, no ha acabado    
    
    def tick_tick_tick(self)->None:
        if self.cerrar_ventana:
            if self.scheduler:
                self.scheduler.pldobc_en_uso = False # Ya regresamos al otro   
                self.scheduler.tick_tick_tick()
                
                self.destroy()
                return
            else:
                self.destroy() # destruye sólo esta si no tenemos scheduler
            return
        
        if self.tarea_actual.estado == "Blocked": 
            self.tarea_actual = self.tIDLE
            self.tarea_actual.estado = "Running"
            
        lista_tareas_listas : list[Tarea]= self.buscar_cuales_estan_listas()
        tarea_de_mayor_prioridad : Tarea|None= self.cual_tiene_mayor_prioridad(
            lista_tareas_listas
            )     
        
        if tarea_de_mayor_prioridad is not None:
            if tarea_de_mayor_prioridad.prioridad > self.tarea_actual.prioridad: # preemption
                
                # Como se dejó a medias se pasa a ready, no blocked
                # Además, los mismos atributos del objeto guardan el tiempo restante
                self.tarea_actual.estado = "Ready"
                
                self.tarea_actual = tarea_de_mayor_prioridad #se cambia la tarea actual a la nueva con mayor prioridad
                self.tarea_actual.estado = "Running" #la tarea que se estará corriendo ahora
                
        # Guarda el mensaje de ejecución en el historial      
        if self.ya_finalizo(self.tarea_actual): # Si ya terminó la tarea
            tiempo_seg = miliseg_a_seg(self.tarea_actual.tiempo_lleva)
            mensaje=f"{self.tarea_actual.id} ha finalizado en {tiempo_seg}"
        else:
            mensaje = self.tarea_actual.ejecutar()
            
        self.meter_mensaje(mensaje=mensaje,donde=self.muestra_tareas) 
        
        # Para evitar spam, se desactivan los botones si la tarea ya está corriendo o en cola
        self.boton_enviar.config(
            state="disabled" if self.tLORA.estado in ["Ready", "Running"]
            else "normal"
        )
        self.boton_fotos.config(
            state="disabled" if self.tMILO.estado in ["Ready", "Running"]
            else "normal"
        )
        self.tiempo_corriendo+=TICK
        if self.tiempo_corriendo>self.tiempo_maximo: # ya dejar de correrlo
            self.cerrar_ventana = True # se cierra en la siguiente vuelta
            
            t = miliseg_a_seg(self.tiempo_maximo)
            self.meter_mensaje(
                f"Se ha ejecutado PLD-OBC de exitosamente durante {t} segundos",
                self.muestra_tareas
            )
            self.meter_mensaje(
                f"Regresando al Scheduler principal",
                self.muestra_tareas
            )
        
        #se vuelve a llamar cuando haya transcurrido el tiempo del tick
        self.after(TICK,self.tick_tick_tick) 
             
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