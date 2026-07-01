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
#   Rutas de imagenes emergencia: 12.6.26
#   Color y font de ventana acerca de: 1.7.26
#   Pasar formato y rutas de imágenes a otro archivo: 1.7.26

TICK = 1000 # Cuánto tarda cada tick en milisegundos
ORBITA = 500.0 # inicial en kilómetros

def miliseg_a_seg(milisegundos:int)->str:
    # Toma un valor en milisegundos y lo convierte a segundos
    # Y lo devuelve en segundos, indicando la nueva unidad de medida en el string
    segundos : float = milisegundos/1000
    return f"{segundos} segundos"