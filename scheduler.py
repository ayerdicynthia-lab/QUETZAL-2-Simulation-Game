# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# ILUSTRACIONES: Cynthia Ayerdi, Natalia Sánchez
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
#   Fecha de creación: 27.5.26
#       - Ejecución según prioridad (preemption)
#       - Todas las tareas deben tener prioridades distintas
#       - Mensajes de ejecución cada tick, se guardan en el historial
#   Mejoras de UX y funcionamiento: 28.5.26
#       - Cambiar descripción por un id más claro
#       - Eliminar el truquito (y todo lo que conllevó) de prioridad = -1 al terminar la tarea
#         para implementar botones de comandos para continuar la funcionalidad
#       - Botones para que el usuario envíe comandos
#       - Implementación de round-robin (tareas con la misma prioridad)
#   PLD-OBC EMERGENCY MODE: 1.6.26
#       - Instanciar la ventana de la clase emergencia en uno de cada 10 comandos
#       - Modificar la ventana para que no sea toda la pantalla completa
#   Comando deorbit: 1.6.26
#       - Evitar "spam" de botones deshabiltándolos si su tarea está lista o corriendo
#   CRASH MODE: 3.6.26
#       - Anunciar que deorbit no desplegó (1 de cada 3)
#       - Asignar el número de intentos necesario para revivirlo pseudoaleatoriamente
#       - Si no se logra revivir después de 20 intentos, apagar forzosamente el satélite
#         y que se deorbite así sin el mecanismo (proceso más lento)
#   Imágenes para operaciones nominales: 11.6.26
#       - para cada tarea
#   Imágenes para CRASH MODE: 12.6.26
# AJUSTES PENDIENTES:
#   - el label de arriba ya no muestre comando, que muestre modo de operación
#     tipo modo de operación nominal, modo de operación payload1...

from tkinter import Tk, Label, Button
from tkinter import scrolledtext as st, Frame, messagebox as msg
from PIL import Image, ImageTk
from random import randint
from constantes import COLOR_FONDO_SCHEDULER,COLOR_LETRA_SCHEDULER
from constantes import COLOR_BOTON,COLOR_LETRA_BOTON
from constantes import FONT_LETRA_SCHEDULER,FONT_LETRITA_SCHEDULER
from constantes import FONT_BOTON_COMANDO,COLOR_BOTON_COMANDO
from constantes import COLOR_LETRA_BOTON_COMANDO,COLOR_LETRA_MENSAJE
from constantes import COLOR_BOTON_EMERGENCY, ORBITA # para el deorbit
from constantes import TICK, miliseg_a_seg, hacer_imagen
from constantes import SCHED_SIMPLE, SCHED_ANTENAS, SCHED_FUEGO
from constantes import SCHED_CAMARA, SCHED_RECOLECTAR_DATOS, SCHED_VERIFICAR
from constantes import SCHED_DEORBIT, SCHED_DEORBIT_FUEGO
from clase_tarea import Tarea
from pldobc_emergency import PLDOBC_EMERGENCY_CONTROL_MODE
        
class Scheduler_Ventana(Tk):
    def __init__ ( 
        self,
        # Las características de las tareas a realizar
        prioridad_recoleccion:int,duracion_recoleccion:int,
        prioridad_capturar:int,duracion_capturar:int,
        prioridad_verificar:int,duracion_verificar:int
    )->None: 
        
        super().__init__()
        
        # Estética: pantalla completa
        self.state('zoomed')
        self.config(bg=COLOR_FONDO_SCHEDULER)
        self.title("Scheduler")
        
        # Un contenedor para centralizar los elementos en la pantalla
        contenedor = Frame(self,bg=COLOR_FONDO_SCHEDULER)
        contenedor.pack(expand=True) 
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_columnconfigure(1, weight=1)
        contenedor.grid_columnconfigure(2, weight=1)
        contenedor.grid_columnconfigure(3, weight=1)
               
        Label(
            contenedor,text="Scheduler del Sistema Operativo en Tiempo Real",
            bg=COLOR_FONDO_SCHEDULER,fg=COLOR_LETRA_SCHEDULER,
            font=FONT_LETRA_SCHEDULER
        ).grid(column=0,row=0,columnspan=4,pady=2)
        
        Button(
            contenedor,
            text="Cerrar Scheduler",font="Arial 12 bold",
            bg=COLOR_BOTON, fg=COLOR_LETRA_BOTON, 
            command=self.destroy
        ).grid(column=0,row=1,columnspan=4,pady=2)
        
        self.actual_mensaje = Label(
            contenedor,bg=COLOR_FONDO_SCHEDULER,fg=COLOR_LETRA_MENSAJE,
            font=FONT_LETRITA_SCHEDULER,text="Desplegando antenas..."
        )
        self.actual_mensaje.grid(column=0,row=2,columnspan=4,pady=2)
        
        Label(
            contenedor,text=f"\n\n\nHISTORIAL",
            bg=COLOR_FONDO_SCHEDULER,fg=COLOR_LETRA_SCHEDULER,
            font=FONT_LETRA_SCHEDULER
        ).grid(column=0,row=3,columnspan=4,pady=2)
        self.mensajes_anteriores = st.ScrolledText(
            contenedor,width=90,height=9,
            font=FONT_LETRITA_SCHEDULER,
            fg=COLOR_LETRA_MENSAJE,
            state='disabled'
            )
        self.mensajes_anteriores.grid(column=0,row=4,columnspan=4,pady=2)
        
        Label(
            contenedor,
            text=f"{" ENVIAR COMANDOS ":-^200}",
            bg=COLOR_FONDO_SCHEDULER,fg=COLOR_LETRA_SCHEDULER,
            font=FONT_LETRITA_SCHEDULER
        ).grid(column=0,row=5,columnspan=4,pady=2)
        
        # Botones para enviar comandos
        self.boton_recolectar = Button(
            contenedor,text="RECOLECTAR DATOS",
            fg=COLOR_LETRA_BOTON_COMANDO,bg=COLOR_BOTON_COMANDO,
            font=FONT_BOTON_COMANDO, width=20,
            command=self.comando_recolectar_datos
        )
        self.boton_recolectar.grid(column=0,row=6,padx=4,pady=2)
        self.boton_tomar_fotos = Button(
            contenedor,text="TOMAR FOTOS",
            fg=COLOR_LETRA_BOTON_COMANDO,bg=COLOR_BOTON_COMANDO,
            font=FONT_BOTON_COMANDO, width=20,
            command=self.comando_tomar_fotos
        )
        self.boton_tomar_fotos.grid(column=1,row=6,padx=4,pady=2)
        self.boton_verificar_fotos = Button(
            contenedor,text="VERIFICAR FOTOS",
            fg=COLOR_LETRA_BOTON_COMANDO,bg=COLOR_BOTON_COMANDO,
            font=FONT_BOTON_COMANDO, width=20,
            command=self.comando_verificar_fotos
        )
        self.boton_verificar_fotos.grid(column=2,row=6,padx=4,pady=2)
        self.boton_deorbit = Button(
            contenedor,text="DEORBITAR SATÉLITE",
            fg=COLOR_LETRA_BOTON_COMANDO,bg=COLOR_BOTON_EMERGENCY,
            font=FONT_BOTON_COMANDO, width=20,
            command=self.comando_deorbit
        )
        self.boton_deorbit.grid(column=3,row=6,padx=4,pady=2)
        
        # - - - ILUSTRACIONES - - -
        
        self.satelite_simple = hacer_imagen(SCHED_SIMPLE, scaling=3.5)
        self.satelite_antenas = hacer_imagen(SCHED_ANTENAS, scaling=5.5)
        self.satelite_camara = hacer_imagen(SCHED_CAMARA, scaling=5.8)
        self.satelite_deorbit = hacer_imagen(SCHED_DEORBIT, scaling=6.6)        
        self.satelite_deorbit_fuego = hacer_imagen(SCHED_DEORBIT_FUEGO, scaling=9.2)
        self.satelite_verifica = hacer_imagen(SCHED_VERIFICAR, scaling=5.5)
        self.satelite_datos = hacer_imagen(SCHED_RECOLECTAR_DATOS,scaling=5.5)
        self.satelite_fuego = hacer_imagen(SCHED_FUEGO,scaling=7)
                
        # Label para mostrar las ilustraciones
        self.muestra_imagenes : Label = Label(
            self,bg=COLOR_FONDO_SCHEDULER,
            image=self.satelite_simple # La inicial
        )
        self.muestra_imagenes.place(x=15,y=10)
        
        # Guardar las tareas con la información enviada en los parámetros
        self.tRecoleccion : Tarea = Tarea(
            prioridad=prioridad_recoleccion,
            id="Recolectar datos del funcionamiento del satélite",
            estado="Blocked",tiempo_restante=duracion_recoleccion,tiempo_lleva=0,
            imagen=self.satelite_datos,label_imagen=self.muestra_imagenes
        )
        self.tCaptura : Tarea = Tarea(
            prioridad=prioridad_capturar,id="Tomar fotos de Guatemala",
            estado="Blocked",tiempo_restante=duracion_capturar,tiempo_lleva=0,
            imagen=self.satelite_camara,label_imagen=self.muestra_imagenes
        )
        self.tVerifica : Tarea = Tarea(
            prioridad=prioridad_verificar,id="Verificar que las fotos no tengan nubes",
            estado="Blocked",tiempo_restante=duracion_verificar,tiempo_lleva=0,
            imagen=self.satelite_verifica,label_imagen=self.muestra_imagenes
        )
        
        # Guardar el tiempo que toma cada tarea para volver lo a usar
        self.tiempo_recoleccion : int = self.tRecoleccion.tiempo_restante
        self.tiempo_captura : int = self.tCaptura.tiempo_restante
        self.tiempo_verifica : int= self.tVerifica.tiempo_restante
        
        # inicializarla sólo para el loop deorbit normal
        # estos intentos son para reactivar el deorbit si falla
        # se asigna un valor sólo si entra al crash mode
        self.intentos_para_revivir=0
        
        self.posicion_round_robin : int = -1
        
        # La tarea de espera que corre cuando no hay nada
        self.tIdle : Tarea = Tarea(
            prioridad=0, 
            id="Esperando",
            estado="Running", # Se inicializa corriendo la tarea de espera
            tiempo_restante=1_000_000, # Truquito: prácticamente que nunca se acaba
            tiempo_lleva=0,
            imagen=self.satelite_antenas,
            label_imagen=self.muestra_imagenes
        )
        self.tDeorbit : Tarea = Tarea(
            prioridad=30,
            id="Deorbitación del satélite",
            estado="a", # Igual no se está tomando en cuenta, va botar todo
            tiempo_restante=10_000,
            tiempo_lleva=0,
            imagen=self.satelite_deorbit,
            label_imagen=self.muestra_imagenes
        )
        
        # Lista de todas las tareas que hay para hacer
        self.tareas = [self.tRecoleccion,self.tCaptura,self.tIdle,self.tVerifica]
        
        # Para la deorbitación del satélite
        self.cerrar_ventana = False
        self.esta_deorbitando = False
        self.orbita = ORBITA # Inicializa la órbita en km del satélite
        
        self.emergencia = False # banderita de si estamos en emergencia
        self.tarea_actual = self.tIdle # Se inicia en la tarea de espera
        self.after(3*TICK,self.tick_tick_tick)
       
    def round_robin(self,tareas_listas:list[Tarea])->None:
        
        # Función para alternar entre tareas de la misma prioridad
        
        # Incrementa la variable global que lleva la posición de cuál se va ejecutando
        self.posicion_round_robin = (self.posicion_round_robin+1) % len(tareas_listas) 
        
        self.tarea_actual.estado = "Ready" # La deja de correr
        tarea_nueva = tareas_listas[self.posicion_round_robin] # La que toca
        self.tarea_actual = tarea_nueva
        self.tarea_actual.estado = "Running"
        
    def comandan(self,tarea:Tarea,tiempo:int)-> None:
        # Función que actualiza el estado de la tarea cuando se comanda que se haga
        # Para que esté ready y se pueda ejecutar según prioridad
        
        tarea.estado = "Ready"
        tarea.tiempo_restante = tiempo # El tiempo que se debe tardar según lo inicializado
        tarea.tiempo_lleva = 0
    
    def emergencia_aleatoria(self)->None:
        num_para_emergencia = randint(1,6)
        if num_para_emergencia == 1: #un número arbitrario
            self.emergencia=True
            
            # Pseudoaleatoriedad para si se va a arreglar o no y si se va a no comms
            arreglar : bool = bool(randint(0,1)) #0 es false y 1 es true
            tiempo_arreglar : int = (randint(10,20)) * 1_000 # en milisegundos
            
            no_comms : bool = bool(randint(0,1)) 
            tiempo_no_comms : int = (randint(10,20)) * 1_000
            
            ventana_emergencia = PLDOBC_EMERGENCY_CONTROL_MODE(
                scheduler=self,
                se_va_a_arreglar=arreglar,
                cuanto_para_arreglarse=tiempo_arreglar,
                se_va_a_pasar_a_no_comms=no_comms,
                cuanto_para_no_comms=tiempo_no_comms
            )
            ventana_emergencia.mainloop()
            
    def comando_deorbit(self)-> None:
        # Comando para activar el mecanismo de deorbit del satélite
        # Para que regrese a la atmósfera sin volverse basura
        
        #Asegurarse que el usuario esté seguro de esto
        respuesta = msg.askyesno("CONFIRMACIÓN","¿Está segur@ que quiere hacer esto?\nYa no hay vuelta atrás")
        
        if not respuesta:
            return
        
        #1 de cada 3 no funciona
        posibilidad = randint(1,3)
        if posibilidad==1:
            #Ingreso a crash mode
            
            #Informarle al usuario
            msg.showwarning("CRASH MODE","No se ha logrado desplegar el mecanismo de deorbit")            
            mensaje1 = "CRASH MODE: Se intentará reactivar el mecanismo de deorbit"
            mensaje2 = "Quedan 20 intentos"
            self.meter_mensaje(mensaje1,self.mensajes_anteriores)
            self.meter_mensaje(mensaje2,self.mensajes_anteriores)
            self.actual_mensaje['text'] = "CRASH MODE !!"
            
            # Aunque no esté realmente funcionando el deorbit se activa esta banderita
            # para que deorbit tome prioridad y deje de correr el resto del scheduler
            self.esta_deorbitando = True 
            
            # cuántos intentos tomará para que se reviva
            # si son más de 20 no se revive
            self.intentos_para_revivir = randint(10,40)
            
            self.intento_actual = 1 #inicializar
            self.after(TICK,self.loop_deorbitar_fallo)
            
        else:
            self.esta_deorbitando = True
            self.after(TICK,self.loop_deorbitar)
        
    def decremento_deorbit(self)->int:
        # Ver en cuánto debe irse decrementando la órbita cada tick dependiendo
        # si es un deorbit con o sin el mecanismo
        
        if self.intentos_para_revivir<=20: #usando el mecanismo
            pasos : int = 10_000 // TICK 
            decremento_por_tick : int = int(ORBITA) // pasos
        else: #crash mode sin mecanismo
            decremento_por_tick = 10 #se deorbita más lento
            
        return decremento_por_tick
        
    def loop_deorbitar_fallo(self):
        # crash mode
        
        # Mensajes que se mostrarán según cada caso
        separador = "- "*85
        
        if self.intento_actual>20:
            mensaje_muerte = f"No se ha logrado activar el deorbit tras 20 intentos."
            mensaje_muerte2=f"Se apagará intencionalmente el satélite"
            
            self.meter_mensaje(separador,self.mensajes_anteriores)
            self.meter_mensaje(mensaje_muerte,self.mensajes_anteriores)
            self.meter_mensaje(mensaje_muerte2,self.mensajes_anteriores)
            self.meter_mensaje(separador,self.mensajes_anteriores)
            
            # ya se va a hacer el deorbit aunque no se haya desplegado el mecanismo
            self.after(TICK,self.loop_deorbitar) 
            
        elif self.intento_actual == self.intentos_para_revivir:
            # se revive
            mensaje_resurreccion = f"¡Se ha logrado activar el mecanismo de deorbit tras {self.intento_actual} intentos!"
            mensaje_resurreccion2 = f"Volviendo al modo de operación normal para deorbit..."
            
            self.meter_mensaje(separador,self.mensajes_anteriores)
            self.meter_mensaje(mensaje_resurreccion,self.mensajes_anteriores)
            self.meter_mensaje(mensaje_resurreccion2,self.mensajes_anteriores)
            self.meter_mensaje(separador,self.mensajes_anteriores)
            
            # ir al modo normal con el deorbit activado
            # tomará en cuenta que los intentos para revivir eran menos que 20
            # por eso funcionará normal
            self.after(TICK,self.loop_deorbitar) 
            
        else:
            # No se logra revivir el deorbit en este intento, seguir probando
            mensaje_intento = f"El intento {self.intento_actual} de reactivar el deorbit no ha funcionado."
            self.meter_mensaje(mensaje_intento,self.mensajes_anteriores)
            
            self.intento_actual+=1 # ir al siguiente intento
            self.after(TICK,self.loop_deorbitar_fallo)
        
    def loop_deorbitar(self):
        # Para que se complete el deorbit
        if self.cerrar_ventana:
            # Hasta en esta siguiente vuelta se va a cerrar
            self.destroy() 
            return
               
        mensaje = "" #Inicializarlo por si acaso
        if self.orbita<=0:
            # Tarea finalizada
            mensaje = f"El satélite se ha deorbitado exitosamente"
            self.cerrar_ventana=True # Ahora se cerrará en la siguiente
        else:
            if self.orbita<=300 and self.intentos_para_revivir<=20:
                self.tDeorbit.imagen = self.satelite_deorbit_fuego 
            
            # casos de shut down en crash mode
            if self.intentos_para_revivir>20 and self.orbita>300:
                self.tDeorbit.imagen = self.satelite_antenas # se deorbita sin mecanismo deorbit
                
            if self.intentos_para_revivir>20 and self.orbita<= 300:
                self.tDeorbit.imagen = self.satelite_fuego #se quema el satélite solito
            
            self.tDeorbit.ejecutar()
            # Ir decrementando la órbita cada tick
            
            # se calculará dependiendo de si es deorbit normal o crash mode sin deorbit
            decremento = self.decremento_deorbit() 
            self.orbita-=decremento
            
            mensaje = f"Deorbitando satélite... Órbita de {self.orbita} km"
            
        self.actual_mensaje['text']=mensaje
        self.meter_mensaje(mensaje,donde=self.mensajes_anteriores)
        self.after(TICK,self.loop_deorbitar)
       
    def comando_recolectar_datos(self)->None:
        self.emergencia_aleatoria() # en cada comando se ve si habrá emergencia pseudoaleatoria   
        self.comandan(tarea=self.tRecoleccion,tiempo=self.tiempo_recoleccion)
        
    def comando_tomar_fotos(self)->None:
        self.emergencia_aleatoria()
        self.comandan(tarea=self.tCaptura,tiempo=self.tiempo_captura)
        
    def comando_verificar_fotos(self)->None:
        self.emergencia_aleatoria()
        self.comandan(tarea=self.tVerifica,tiempo=self.tiempo_verifica)
        
    def buscar_cuales_estan_listas(self)->list[Tarea]:
        # De la lista de tareas encuentra cuáles están en un estado ready
        # Y las devuelve en una lista
        
        tareitas_listas : list[Tarea] = [] # Inicializar la lista de tareas que están listas
        for tarea in self.tareas:
            
            if tarea.estado == "Ready" or tarea.estado=="Running":
                # Agrega sólo las tareas ready a la lista de tareas ready.
                tareitas_listas.append(tarea) 
                
        return tareitas_listas
    
    def cuales_tienen_mayor_prioridad(self,tareas_listas:list[Tarea])->list[Tarea]:
        # Devuelve una lista de las tareas que se encuentran ready que tengan más prioridad
        
        # Si no hay tareas listas, ni hay que meterse a ver cuál tiene más prioridad
        # Porque no hay nada
        if len(tareas_listas)==0:
            return []
        
        mayor_prioridad = tareas_listas[0].prioridad #asumir que la primera tiene mayor prioridad
        candidatas = [tareas_listas[0]] #poniendola como tarea lista al inicio
        for tarea in tareas_listas[1:]: #desde el segundo elemento
            
            # Si hay una tarea que ya no tiene tiempo restante es porque ya acabó
            # Ya no hay que tomarla en cuenta
            if tarea.tiempo_restante >= 0: 
                
                if tarea.prioridad > mayor_prioridad: #tiene más prioridad que la que más tenía hasta ese momento
                    mayor_prioridad = tarea.prioridad #nuevo mayor
                    candidatas = [ tarea ] #nueva tarea
                elif tarea.prioridad == mayor_prioridad: #la misma prioridad
                    candidatas.append(tarea) #Ahora hay varias candidatas
        return candidatas                
        
    def ya_finalizo(self,tarea:Tarea)->bool:
        # Verifica si una tarea ha finalizado
        # Comprueba si ya no hay tiempo restante de ejecución
        
        if tarea.tiempo_restante <= 0: # Ya no queda nada "por hacer"
            tarea.estado = "Blocked" #después veremos funcionalidad de esto
            return True # Se acabó
        
        return False # Si aún hay tiempo, no ha acabado
    
    def meter_mensaje(self,mensaje:str,donde:st.ScrolledText)->None:
        # Para colocar el mensaje en el historial
        
        donde.config(state="normal")
        donde.insert("end",f"{mensaje}\n")
        donde.config(state="disabled")
        donde.see("end") # Baja al final del texto
        
    def tick_tick_tick(self)->None:
        
        if self.emergencia:
            # Pausar el scheduler si estamos en emergencia
            return
        
        if self.esta_deorbitando:
            # No hacer más tareas que la deorbitación
            
            # Lo podríamos hacer con prioridad máxima tmbién
            # Pero ya está de esta manera en PLDOBC emergency
            
            #desactivar botones
            self.boton_verificar_fotos.config(state="disabled")
            self.boton_tomar_fotos.config(state="disabled")
            self.boton_recolectar.config(state="disabled")
            self.boton_deorbit.config(state="disabled")
            return
        
        # Para que no la siga tomando en cuenta si se acabó
        if self.tarea_actual.estado == "Blocked": 
            self.tarea_actual = self.tIdle
            self.tarea_actual.estado = "Running"
        
        # Identificar las tareas de mayor prioridad listas para correr
        lista_tareas_listas : list[Tarea]= self.buscar_cuales_estan_listas()
        tareas_de_mayor_prioridad : list[Tarea]= self.cuales_tienen_mayor_prioridad(
            lista_tareas_listas
            )
        
        if len(tareas_de_mayor_prioridad)==1:
            tarea_nueva : Tarea = tareas_de_mayor_prioridad[0] #el único elemento
            if tarea_nueva.prioridad > self.tarea_actual.prioridad:
                
                # Como se dejó a medias se pasa a ready, no blocked
                # Además, los mismos atributos del objeto guardan el tiempo restante
                self.tarea_actual.estado = "Ready"
                
                self.tarea_actual = tarea_nueva #se cambia la tarea actual a la nueva con mayor prioridad
                self.tarea_actual.estado = "Running" #la tarea que se estará corriendo ahora
                
        elif len(tareas_de_mayor_prioridad)>1: # Round robin como hay varias con la misma prioridad.
            self.round_robin(tareas_de_mayor_prioridad)
        
        # Guarda el mensaje anterior en el historial        
        self.meter_mensaje(mensaje=self.actual_mensaje['text'],donde=self.mensajes_anteriores) 
        
        # Actualiza el mensajito actual
        # Ejecutar tarea mostrando cuánto tiempo se lleva ejecutando
        mensaje = self.tarea_actual.ejecutar() 
        self.actual_mensaje['text'] = mensaje
        
        if self.ya_finalizo(self.tarea_actual): # Si ya terminó la tarea
            tiempo_seg = miliseg_a_seg(self.tarea_actual.tiempo_lleva)
            self.actual_mensaje['text']=f"{self.tarea_actual.id} ha finalizado en {tiempo_seg}"
            
        # Para evitar spam, se desactivan los botones si la tarea ya está corriendo o en cola
        self.boton_recolectar.config(
            state="disabled" if self.tRecoleccion.estado in ["Ready", "Running"]
            else "normal"
        )
        self.boton_tomar_fotos.config(
            state="disabled" if self.tCaptura.estado in ["Ready", "Running"]
            else "normal"
        )
        self.boton_verificar_fotos.config(
            state="disabled" if self.tVerifica.estado in ["Ready", "Running"]
            else "normal"
        )
            
        self.after(TICK,self.tick_tick_tick) #se vuelve a llamar cuando haya transcurrido ese tiempo
       
if __name__ == "__main__": 
    scheduler = Scheduler_Ventana(
        prioridad_recoleccion=1, duracion_recoleccion= 5_000,
        prioridad_capturar= 2, duracion_capturar= 3_000,
        prioridad_verificar=1, duracion_verificar=4_000
    )
    scheduler.mainloop()