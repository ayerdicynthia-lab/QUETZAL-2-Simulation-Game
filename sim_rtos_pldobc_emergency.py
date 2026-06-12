# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Interfaz toplevel para una emergencia pseudoaleatoria donde la computadora
# principal del satélite deja de funcionar y la computadora hecha en casa debe tomar el mando.
# Incluye una emergencia posible y peor: la falla de comunicación con la PLD-OBC.
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA:
#   Fecha de creación: 1.6.26
#       - Pseudoaleatoriedad para arreglarse y/o irse a no comms
#       - Las tareas se ejecutan repetitivamente con duraciones pseudoaleatorias
#       - Permite que el usuario deorbite el satélite
#       - Mande mensajes diciendo "cómo está", pidiendo ayuda
#   Crash mode: 5.6.26
#       - No funciona el despliegue del deorbit en el no comms
#   Imágenes: 12.6.26

from tkinter import Toplevel, Label, messagebox as msg, Button, scrolledtext as st
from random import randint
from sim_rtos_constantes import FONT_LETRA_EMERGENCY, COLOR_LETRA_EMERGENCY, TICK
from sim_rtos_constantes import FONT_LETRITA_EMERGENCY, COLOR_FONDO_EMERGENCY, ORBITA
from sim_rtos_constantes import COLOR_LETRA_BOTON, COLOR_BOTON_EMERGENCY
from sim_rtos_constantes import RUTA_EMERGENCY_1, RUTA_EMERGENCY_2, RUTA_EMERGENCY_3
from sim_rtos_constantes import RUTA_EMERGENCY_4, RUTA_EMERGENCY_5, RUTA_EMERGENCY_6
from sim_rtos_constantes import hacer_imagen
from sim_rtos_tarea import Tarea

class PLDOBC_EMERGENCY_CONTROL_MODE(Toplevel): # Será una ventanita que se abrirá
    def __init__(
        self,
        scheduler, # para poder modificar su estado
        se_va_a_arreglar : bool,
        cuanto_para_arreglarse : int, # En milisegundos
        se_va_a_pasar_a_no_comms : bool,
        cuanto_para_no_comms : int
    ) -> None:
        super().__init__(scheduler) #Master
        
        self.geometry("800x640+20+20")
        self.config(bg=COLOR_FONDO_EMERGENCY)
        self.title("Emergencia")
                
        # --- ILUSTRACIONES ---
        self.imagen_ayuda = hacer_imagen(RUTA_EMERGENCY_1,scaling=5.8)
        self.imagen_fotos = hacer_imagen(RUTA_EMERGENCY_2,scaling=5.8)
        self.imagen_verificar = hacer_imagen(RUTA_EMERGENCY_3,scaling=5.8)
        self.imagen_deorbit = hacer_imagen(RUTA_EMERGENCY_4,scaling=6.7)
        self.imagen_deorbit_fuego = hacer_imagen(RUTA_EMERGENCY_5,scaling=8.8)
        self.imagen_satelite_fuego = hacer_imagen(RUTA_EMERGENCY_6,scaling=6.8)
        
        # label para poner imagen
        self.muestra_imagenes : Label = Label(
            self,bg=COLOR_FONDO_EMERGENCY,
            image=self.imagen_ayuda, # La inicial
            height=290
        )
        self.muestra_imagenes.pack()
        
        Label(
            self,
            text="LA COMPUTADORA PRINCIPAL HA FALLADO",
            font=FONT_LETRA_EMERGENCY,
            bg=COLOR_FONDO_EMERGENCY,
            fg=COLOR_LETRA_EMERGENCY
        ).pack(pady=2)
        
        self.muestra_mensajes : st.ScrolledText = st.ScrolledText(
            self,width=63,height=10,
            font=FONT_LETRITA_EMERGENCY
        )
        self.muestra_mensajes.pack(pady=2)
        
        # Guardar estos parámetros
        self.scheduler = scheduler
        self.se_va_arreglar : bool = se_va_a_arreglar
        self.pasar_a_no_comms : bool = se_va_a_pasar_a_no_comms
        if (se_va_a_arreglar == True) and (cuanto_para_arreglarse<cuanto_para_no_comms):
            # Para ahorrarle trabajo a la compu de que si igual se arregla
            # Antes de que pase a no comms ni lo trate de hacer
            self.pasar_a_no_comms=False
            
        if self.se_va_arreglar:
            # Sólo importa cuánto se va a tardar en arreglarse si sí pasará
            self.cuanto_para_arreglarse : int | None = cuanto_para_arreglarse
        else:
            # Si no se va a arreglar pues lástima
            self.cuanto_para_arreglarse = None
        
        if self.pasar_a_no_comms:
            self.cuanto_para_no_comms : int | None= cuanto_para_no_comms
        else:
            self.cuanto_para_no_comms = None
               
        # Las tareitas que se van a estar ejecutando
        tTomarFotos: Tarea = Tarea(
            prioridad=0,
            id="Intentando tomar fotos",
            estado="a",
            tiempo_restante=6_000,
            tiempo_lleva=0,
            imagen=self.imagen_fotos,
            label_imagen=self.muestra_imagenes
        )
        tVerificarFotos: Tarea = Tarea(
            prioridad=1,
            id="Intentando verificar las fotos",
            estado="a",
            tiempo_restante=5_000,
            tiempo_lleva=0,
            imagen=self.imagen_verificar,
            label_imagen=self.muestra_imagenes
        )
        tRevivirCompu : Tarea = Tarea(
            prioridad=1,
            id="Intentando revivir la computadora principal",
            estado="a",
            tiempo_restante=6_000,
            tiempo_lleva=0,
            imagen=self.imagen_ayuda, # por ahora,
            label_imagen=self.muestra_imagenes
        )
        
        # Comando y tarea deorbit
        self.boton_deorbit = Button(
            self, text="Deorbitar satélite",
            fg=COLOR_LETRA_BOTON,bg=COLOR_BOTON_EMERGENCY,
            font=FONT_LETRITA_EMERGENCY,
            command=self.deorbitar
        )
        self.boton_deorbit.pack(pady=2)
        self.tDeorbit : Tarea = Tarea(
            prioridad=3,
            id="Deorbitación del satélite",
            estado="a",
            tiempo_restante=10_000,
            tiempo_lleva=0,
            imagen=self.imagen_deorbit,
            label_imagen=self.muestra_imagenes
        )
        
        # Mensajes iniciales
        # se muestran después de poner las cosas en la ventana
        msg.showerror("ERROR GRAVE","Error en la computadora principal del satélite")
        msg.showinfo("MODO DE OPERACIÓN","Se utilizará el modo de operación de emergencia\na cargo de la computadora hecha en UVG")
        
        # Las que van a pasar por el loopcito
        # El deorbit pasa sólo si lo mandan a hacer
        self.tareas_repetitivas : list[Tarea] = [
            tTomarFotos,tVerificarFotos,tRevivirCompu
        ]
        self.pos_tareas : int = 0 #En qué tarea de la listita vamos
        
        # para cuando hay no comms
        self.caracteres_ofuscadores : str = ")1#°.$!4a :2ï >3%;|p=7) 5?ñ¿¡*¨9%?} {ö/]-:<"
        self.pos_caracteres_ofuscadores: int = 0 
        self.cada_cuantos_ofusca = 6
        self.intento_actual= 0
        self.intentos_para_revivir = randint(15,30)
        
        self.cerrar_ventana = False
        self.esta_deorbitando = False
        self.orbita = ORBITA # Inicializa la órbita en km del satélite
        self.tiempo = 0 # Para poder ver cuándo es momento de arreglar o pasar a no comms
        self.after(TICK,self.loop_loop)
        
    def meter_mensaje(self,mensaje:str,donde:st.ScrolledText)->None:
        # Para colocar el mensaje en donde va a mostrarse
        
        donde.config(state="normal")
        donde.insert("end",f"{mensaje}\n")
        donde.config(state="disabled")
        donde.see("end") # Baja al final del texto
        
    def deorbitar(self)->None:
        # Comando para activar el mecanismo de deorbit del satélite
        # Para que regrese a la atmósfera sin volverse basura
        
        #Asegurarse que el usuario esté seguro de esto
        respuesta = msg.askyesno(
            "CONFIRMACIÓN",
            "¿Está segur@ que quiere hacer esto?\nYa no hay vuelta atrás")
        
        if not respuesta:
            return
        
        self.boton_deorbit.config(state="disabled") # para que no lo spamee
        self.esta_deorbitando = True
        self.after(TICK,self.loop_deorbitar)
        
    def decremento_deorbit(self)->int:
        # Ver en cuánto debe irse decrementando la órbita cada tick dependiendo
        # si es un deorbit con o sin el mecanismo
        
        if self.intentos_para_revivir<=20: #usando el mecanismo, lo normal
            pasos : int = 10_000 // TICK 
            decremento_por_tick : int = int(ORBITA) // pasos
        else: #crash mode sin mecanismo
            decremento_por_tick = 10 #se deorbita más lento
            
        return decremento_por_tick
        
    def loop_deorbitar(self)->None: 
        # Para que se complete el deorbit
        if self.cerrar_ventana:
            # Hasta en esta siguiente vuelta se va a cerrar
            if self.scheduler:
                self.scheduler.destroy() # Destruye la ventana principal (entonces esta también)
            else:
                self.destroy() # destruye sólo esta si no tenemos scheduler
            return
        
        mensaje = "" #Inicializarlo por si acaso
        if self.orbita<=0:
            # Tarea finalizada
            mensaje = f"El satélite se ha deorbitado exitosamente"
            self.cerrar_ventana=True # Ahora se cerrará en la siguiente
                       
        else:
            
            if self.orbita <= 300 and self.intentos_para_revivir<=20: # se usa el mecanismo normal
                self.tDeorbit.imagen = self.imagen_deorbit_fuego
                
            # casos de shut down en crash mode
            if self.intentos_para_revivir>20 and self.orbita>300:
                self.tDeorbit.imagen = self.imagen_ayuda # se deorbita sin mecanismo deorbit
                
            if self.intentos_para_revivir>20 and self.orbita<= 300:
                self.tDeorbit.imagen = self.imagen_satelite_fuego #se quema el satélite solito
            
            self.tDeorbit.ejecutar()
            # Ir decrementando la órbita cada tick
            
            # se calculará dependiendo de si es deorbit normal o crash mode sin deorbit
            decremento = self.decremento_deorbit() 
            self.orbita-=decremento
            
            mensaje = f"Deorbitando satélite... Órbita de {self.orbita} km"
            
        self.meter_mensaje(mensaje,donde=self.muestra_mensajes)
        
        # No aumentar el contador de tiempo para arreglar o no comms
        # Porque igual ya no hay nada más acá
        self.after(TICK,self.loop_deorbitar)
        
    def informar_que_esta_mal(self):
        mensaje = f"AYUDA: La computadora principal no ha funcionado por {self.tiempo//1000} segundos"
        self.meter_mensaje(mensaje,self.muestra_mensajes)
        self.muestra_imagenes.config(image=self.imagen_ayuda) # para que la muestre en ese tick
        
    def ofuscar(self,mensaje:str)->str:
        lista_caracteres_mensaje = list(mensaje)
        
        for i in range (len(mensaje)):
            if ((i%self.cada_cuantos_ofusca)==0) or (self.cada_cuantos_ofusca<=1):
                #Para que vaya ofuscando cada ciertos caracteres
                # y cuando esto sea menor a 1 ya se ofusquen todos
                lista_caracteres_mensaje[i]=self.caracteres_ofuscadores[self.pos_caracteres_ofuscadores]
                
                self.pos_caracteres_ofuscadores=randint(1,len(self.caracteres_ofuscadores)-1) #cambiando que caracter ofuscará
                
        return "".join(lista_caracteres_mensaje)
        
    def loop_loop(self)->None:
        # Como el scheduler del otro pero acá no nos estamos enfocando
        # En su cosa de prioridades
        
        if self.esta_deorbitando:
            # No seguir ejecutando cosas si ya se está deorbitando
            return
        
        if isinstance(self.cuanto_para_arreglarse , int) and (self.tiempo>= self.cuanto_para_arreglarse): 
            #Si es un entero (no None) y ya es hora que se arregle
            if self.cerrar_ventana:
                
                # Volver a activar el scheduler
                if self.scheduler:
                    self.scheduler.emergencia = False # Ya no hay emergencia   
                    self.scheduler.tick_tick_tick()
                
                self.destroy()
                return
            
            self.cerrar_ventana = True # para que se cierre hasta la siguiente vuelta
            
            # Mensajes a colocar
            linitas = "- "*45 # separador
            exito = "¡SE HA LOGRADO REESTABLECER LA COMPUTADORA PRINCIPAL!"
            nominal = "Regresando al MODO DE OPERACIÓN nominal..."
            
            self.meter_mensaje(linitas,self.muestra_mensajes)
            self.meter_mensaje(exito,self.muestra_mensajes)
            self.meter_mensaje(nominal,self.muestra_mensajes)
            self.meter_mensaje(linitas,self.muestra_mensajes)
            self.after(4_000,self.loop_loop) # 4 segundos de espera para la vuelta de cerrar
            return
        
        if (self.tiempo // TICK) % 5 == 2:
            # alega cada 5 vueltitas
            self.informar_que_esta_mal()
            self.tiempo += TICK #Aumentando cuánto tiempo va
            self.after(TICK,self.loop_loop)
            return
        
        # Ejecutar la tarea que toca según la listita
        # Acá no estamos tomando en cuenta las prioridades
        tarea_actual:Tarea=self.tareas_repetitivas[self.pos_tareas]
        mensaje : str = ""
        if tarea_actual.tiempo_restante<=0:
            # Sumarle un segundo como "truquito" para que finalice un segundo 
            # después que la última actualización
            mensaje = f"{tarea_actual.id} finalizó en {(tarea_actual.tiempo_lleva+1000)//1_000} segundos"
            
            # Reiniciar los tiempos de la tarea
            nuevo_tiempo = randint(1,9)
            tarea_actual.tiempo_restante = nuevo_tiempo*1_000 # En milisegundos
            tarea_actual.tiempo_lleva = 0
            
            # Avanzar la posición según corresponde
            self.pos_tareas = (self.pos_tareas+1)%len(self.tareas_repetitivas)
        else:    
            mensaje = tarea_actual.ejecutar()
            
        if isinstance(self.cuanto_para_no_comms, int) and (self.tiempo>=self.cuanto_para_no_comms):
            #Si es un entero (no None) y ya es hora que se pierda la comunicación
            
            # No hay comunicación, no le podemos pedir que haga deorbit
            self.boton_deorbit.config(state="disabled") 
            mensaje = self.ofuscar(mensaje)
            
            # para que se vayan ofuscando cada vez mas
            if self.cada_cuantos_ofusca>1: #que no llegue a zerodivisionerror
                self.cada_cuantos_ofusca-=1
                
            if self.tiempo > 40_000: # después de 40 segundos que trate de hacer deorbit
                self.intento_actual=1
                self.esta_deorbitando=True
                self.after(TICK,self.loop_deorbitar_fallo)
            
        self.meter_mensaje(mensaje,donde=self.muestra_mensajes)
        
        self.tiempo += TICK #Aumentando cuánto tiempo va
        self.after(TICK,self.loop_loop)
    
    def loop_deorbitar_fallo(self):
        # crash mode
        
        # Mensajes que se mostrarán según cada caso
        separador = "- "*45
        
        if self.intento_actual>20:
            mensaje_muerte = f"No se ha logrado activar el deorbit tras 20 intentos."
            mensaje_muerte2 = f"Se apagará intencionalmente el satélite"
            
            self.meter_mensaje(separador,self.muestra_mensajes)
            self.meter_mensaje(mensaje_muerte,self.muestra_mensajes)
            self.meter_mensaje(mensaje_muerte2,self.muestra_mensajes)
            self.meter_mensaje(separador,self.muestra_mensajes)
            
            # ya se va a hacer el deorbit aunque no se haya desplegado el mecanismo
            self.after(TICK,self.loop_deorbitar) 
            
        elif self.intento_actual == self.intentos_para_revivir:
            # se revive
            mensaje_resurreccion = f"¡Se ha logrado activar el mecanismo de deorbit tras {self.intento_actual} intentos!"
            mensaje_resurreccion2 = f"Volviendo al modo de operación normal para deorbit..."
            
            self.meter_mensaje(separador,self.muestra_mensajes)
            self.meter_mensaje(mensaje_resurreccion,self.muestra_mensajes)
            self.meter_mensaje(mensaje_resurreccion2,self.muestra_mensajes)
            self.meter_mensaje(separador,self.muestra_mensajes)
            
            # ir al modo normal con el deorbit activado
            # tomará en cuenta que los intentos para revivir eran menos que 20
            # por eso funcionará normal
            self.after(TICK,self.loop_deorbitar) 
            
        else:
            # No se logra revivir el deorbit en este intento, seguir probando
            mensaje_intento = f"El intento {self.intento_actual} de reactivar el deorbit no ha funcionado."
            self.meter_mensaje(mensaje_intento,self.muestra_mensajes)
            
            self.intento_actual+=1 # ir al siguiente intento
            self.after(TICK,self.loop_deorbitar_fallo)
            
if __name__ == "__main__":
    arreglar : bool = bool(randint(0,1))
    tiempo_arreglar : int = randint(10,20) * 1_000 # Multiplica por mil porque son milisegundos
    
    no_comms : bool = bool(randint(0,1))
    tiempo_no_comms : int = randint(5,20) * 1_000 # Multiplica por mil porque son milisegundos
    
    emergencia = PLDOBC_EMERGENCY_CONTROL_MODE(
        scheduler=None,
        se_va_a_arreglar=arreglar,
        cuanto_para_arreglarse=tiempo_arreglar,
        se_va_a_pasar_a_no_comms=no_comms,
        cuanto_para_no_comms=tiempo_no_comms
    )
    emergencia.mainloop()