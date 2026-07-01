# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Constantes para las rutas de las ilustraciones usadas en los programas
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA
#   Separación del archivo general constantes: 1.7.26

import os
from PIL import Image, ImageTk

# Ruta a la carpeta de este archivo
CARPETA_ACTUAL = os.path.dirname(__file__)

# Ilustraciones - rutas con todo y carpeta para que sí las encuentre
SCHED_SIMPLE = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_simple.png")
SCHED_ANTENAS = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_antenas.png")
SCHED_CAMARA = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_camara.png")
SCHED_DEORBIT = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_deorbit.png")
SCHED_DEORBIT_FUEGO = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_deorbit_fuego.png")
SCHED_VERIFICAR = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_verificar.png")
SCHED_RECOLECTAR_DATOS = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_datos.png")
SCHED_FUEGO = os.path.join(CARPETA_ACTUAL, "scheduler_antenas_fuego.png")

SELECT_SIMPLE = os.path.join(CARPETA_ACTUAL, "select_quetzal2_simple.png")
SELECT_ANTENAS = os.path.join(CARPETA_ACTUAL, "select_quetzal2_antenas.png")
SELECT_DEORBIT = os.path.join(CARPETA_ACTUAL, "select_deorbit_fuego.png")

EMERGENCY_HELP = os.path.join(CARPETA_ACTUAL, "emergency_help.png")
EMERGENCY_CAMARA = os.path.join(CARPETA_ACTUAL, "emergency_camara.png")
EMERGENCY_VERIFICAR = os.path.join(CARPETA_ACTUAL, "emergency_verificar.png")
EMERGENCY_DEORBIT = os.path.join(CARPETA_ACTUAL, "emergency_deorbit.png")
EMERGENCY_DEORBIT_FUEGO = os.path.join(CARPETA_ACTUAL, "emergency_deorbit_fuego.png")
EMERGENCY_FUEGO = os.path.join(CARPETA_ACTUAL, "emergency_antenas_fuego.png")

def hacer_imagen (ruta:str,scaling:float)->ImageTk.PhotoImage:
    # retorna la imagen con el tipo de dato y dimensiones correctas
            
    imagen_inicial = Image.open(ruta)
    ancho, alto = imagen_inicial.size # obtener medidas para luego achiquitar la imagen
    
    #dividirlo entre el scaling factor ahi para que quede bien el tamaño
    ancho = int(ancho//scaling) 
    alto = int(alto//scaling)
    imagen_nuevo_tamano = imagen_inicial.resize( #cambiar tamaño
        (ancho,alto)
    ) 
    return ImageTk.PhotoImage(imagen_nuevo_tamano)