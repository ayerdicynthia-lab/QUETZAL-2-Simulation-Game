# =============================================================================================
# --------------------------------- DOCUMENTACIÓN INTERNA -------------------------------------
# =============================================================================================
# AUTOR: Cynthia Ayerdi. 
#   e12.cynthiamaria.ayerdih@suizoamericano.edu.gt / ayerdicynthia@gmail.com
# ASESORÍA: Luis Carranza, Kuk Ho Chung
# FIN EN MENTE: Crear una simulación didáctica de la computadora de Quetzal-2
# DESCRIPCIÓN: Constantes de forma y algunas funcionalidades usadas a lo largo de los distintos
# scripts del simulador
# LENGUAJE: Python 3.14
# RECURSOS: Intérprete de Python 3.14
# PROCESOS PREVIOS: N/A
# HISTORIA
#   Fecha de creación: 27.5.26
#       - Colores y fonts
#       - Tiempo del tick
#   Función conversión de milisegundos a segundos: 28.5.26
#   Color y formato para botones de comandos: 28.5.26
#   Color y formato para modo de operación de emergencia: 1.6.26
#       - Valor inicial de la órbita
#   Rutas de imagenes: 11.6.26
#       - Operaciones nominales del scheduler
#       - Introductorias en el select

import os
from PIL import Image, ImageTk

TICK = 1000 # Cuánto tarda cada tick en milisegundos
ORBITA = 500.0 # inicial en kilómetros

# Constantes de colores usados en el seleccionador y en el scheduler
COLOR_BOTON = "#B01414"
COLOR_LETRA_BOTON = "#F3EDED"

# Constantes de colores y fonts del scheduler
COLOR_FONDO_SCHEDULER = "#e3ecf7"
COLOR_LETRA_SCHEDULER = "#111262"
FONT_LETRA_SCHEDULER = "Calibri 28 bold"
FONT_LETRITA_SCHEDULER = "Calibri 18 bold"
COLOR_BOTON_COMANDO = "#1C6909"
COLOR_LETRA_BOTON_COMANDO = "#DAEDC5"
FONT_BOTON_COMANDO = "Helvetica 18 bold"
COLOR_LETRA_MENSAJE = "#0E5C48"

# Constantes de colores y fonts del seleccionador
COLOR_FONDO_SELECT = "#A0F1D5"
COLOR_LETRA_SELECT = "#040632"
FONT_LETRA_SELECT = "Arial 20 bold"
FONT_LETRITA_SELECT = "Arial 16 bold"
COLOR_LETRITA_SELECT = "#32347B"

# Constantes de colores y fonts del cosito de emergencia
COLOR_FONDO_EMERGENCY = "#F72128"
COLOR_LETRA_EMERGENCY = "#530407"
COLOR_BOTON_EMERGENCY = "#302929"
FONT_LETRA_EMERGENCY = "Helvetica 20 bold"
FONT_LETRITA_EMERGENCY = "Helvetica 16 bold"

# Ruta a la carpeta de este archivo
CARPETA_ACTUAL = os.path.dirname(__file__)

# Ilustraciones - rutas con todo y carpeta para que sí las encuentre
RUTA_SATELITE_1_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_simple.png")
RUTA_SATELITE_2_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_antenas.png")
RUTA_SATELITE_3_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_camara.png")
RUTA_SATELITE_4_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_deorbit.png")
RUTA_SATELITE_5_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_deorbit_fuego.png")
RUTA_SATELITE_6_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_verificar.png")
RUTA_SATELITE_7_SCHED = os.path.join(CARPETA_ACTUAL, "scheduler_quetzal2_datos.png")

RUTA_SATELITE_1_SELECT = os.path.join(CARPETA_ACTUAL, "select_quetzal2_simple.png")
RUTA_SATELITE_2_SELECT = os.path.join(CARPETA_ACTUAL, "select_quetzal2_antenas.png")
RUTA_SATELITE_4_SELECT = os.path.join(CARPETA_ACTUAL, "select_deorbit_fuego.png")

RUTA_EMERGENCY_1 = os.path.join(CARPETA_ACTUAL, "emergency_help.png")

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

def miliseg_a_seg(milisegundos:int)->str:
    # Toma un valor en milisegundos y lo convierte a segundos
    # Y lo devuelve en segundos, indicando la nueva unidad de medida en el string
    segundos : float = milisegundos/1000
    return f"{segundos} segundos"