#!/usr/bin/env python
# coding: utf-8

import numpy as np
import yt
# Baja el nivel de log para evitar mensajes innecesarios de yt
yt.funcs.mylog.setLevel(50) 
import os 
import cv2
import glob
from pathlib import Path


# --- 1. CONFIGURACIÓN Y GENERACIÓN DE IMÁGENES (FRAMES) ---

# Definición de unidades y caja de contorno (Bounding Box)
unit_base = {
    "UnitLength_in_cm": 3.08568e21, # ~1 kpc, típico para Gadget2/yt
    "UnitMass_in_g": 1.989e43,
    "UnitVelocity_in_cm_per_s": 100000,
}

bbox_lim = 15  # kpc
bbox = [[-bbox_lim, bbox_lim], [-bbox_lim, bbox_lim], [-bbox_lim, bbox_lim]]


# Bucle para procesar los 30 snapshots (del 000.0 al 029.0)
for x in range (30): 
    fname = f"snapshot_{x:03d}.0"
    print(f'Procesando y generando imagen para: {fname}')

    # Cargar el snapshot actual. ESTO DEBE ESTAR DENTRO DEL BUCLE.
    try:
        ds = yt.load(fname, unit_base=unit_base, bounding_box=bbox, ptype_spec="default")
        ds.index
        ad = ds.all_data()

        # Generar el ParticlePlot (Posición X vs. Posición Y) para todas las partículas.
        p = yt.ParticlePlot(ds, ("all", "particle_velocity_z"), ("all", "particle_position_z"), color="b")
        
        # Guardar la imagen (.png). Se guarda en el directorio actual.
        p.save()
    except Exception as e:
        print(f"ERROR al procesar {fname}: {e}")
        # Continuar con el siguiente snapshot si este falla
        continue 
    
print("\n--- Generación de 30 imágenes completada ---")


# --- 2. CREACIÓN DEL VIDEO ---

video_name = 'video3poszvelz.avi'

# Buscar todos los archivos PNG generados en el directorio actual
images = glob.glob('*.png')
print(f"\nSe encontraron {len(images)} archivos PNG.")

if not images:
    print("ERROR: No se encontraron archivos PNG. Asegúrate de que se generaron correctamente.")
else:
    # Cargar la primera imagen para obtener el tamaño (¡Aquí estaba el error de ruta!)
    # Al usar solo 'images[0]', buscamos la imagen en el directorio actual.
    frame = cv2.imread(images[0])
    
    # Comprobación de seguridad para evitar el error 'NoneType'
    if frame is None:
        print(f"ERROR: No se pudo cargar la imagen inicial '{images[0]}'. No se puede crear el video.")
    else:
        # Obtener dimensiones
        height, width, layers = frame.shape
        
        # Crear el objeto VideoWriter: 
        # Tercer parámetro: 10 FPS (10 fotogramas por segundo) para un movimiento más fluido
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MJPG'), 1, (width, height))
        
        print("Creando video...")

        # Escribir todas las imágenes en orden cronológico
        for image in sorted(images):
            # Cargar la imagen y escribirla en el video
            video.write(cv2.imread(image))
        
        # Finalizar y guardar el video
        cv2.destroyAllWindows()
        video.release()
        print(f"¡Video '{video_name}' creado exitosamente con {len(images)} frames!")