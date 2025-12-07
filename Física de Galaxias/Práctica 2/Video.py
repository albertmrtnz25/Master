import numpy as np
import matplotlib.pyplot as plt
import os
import struct
import cv2  # Usamos OpenCV en lugar de MoviePy
import glob
from tqdm import tqdm # Barra de progreso

# --- CONFIGURACIÓN ---
INPUT_DIR = "output_B"           # Carpeta con los datos
OUTPUT_IMG_DIR = "fotogramas_B"  # Carpeta temporal para imágenes
VIDEO_NAME = "evolucion_galaxia_B.avi" # Usamos .avi que es más compatible por defecto
LIMIT_KPC = 15.0                 # Zoom del gráfico (kpc)

# Aseguramos que existe la carpeta de fotos
if not os.path.exists(OUTPUT_IMG_DIR):
    os.makedirs(OUTPUT_IMG_DIR)

# --- FUNCIONES DE LECTURA DE GADGET (BINARIO) ---
def read_gadget_snapshot(filename):
    """
    Lee un archivo binario estándar de Gadget-2 (Format 1).
    Devuelve el tiempo y las posiciones de las partículas del DISCO.
    """
    if not os.path.exists(filename):
        return None, None

    with open(filename, 'rb') as f:
        # 1. LEER CABECERA
        # Bloque HEAD
        dummy = struct.unpack('i', f.read(4))[0] 
        if dummy != 256:
            return None, None
            
        # Leemos npart (cuántas partículas de cada tipo hay)
        npart = np.fromfile(f, dtype=np.int32, count=6)
        
        # Leemos masa 
        massarr = np.fromfile(f, dtype=np.float64, count=6)
        
        # Leemos tiempo
        time = struct.unpack('d', f.read(8))[0]
        
        # Saltamos el resto de la cabecera
        # Hemos leído: 24 + 48 + 8 = 80 bytes. Faltan 256 - 80 + 8 (redshift) = 176 bytes + cierre
        f.seek(256 - 80, 1) 
        
        dummy = struct.unpack('i', f.read(4))[0] # Cierre del bloque HEAD

        # 2. LEER POSICIONES
        # Bloque POS
        dummy = struct.unpack('i', f.read(4))[0] # Apertura bloque POS
        
        # El total de partículas es la suma de npart
        n_total = np.sum(npart)
        
        # Leemos todas las posiciones (3 floats por partícula: x, y, z)
        pos = np.fromfile(f, dtype=np.float32, count=n_total*3).reshape(-1, 3)
        
        # --- SELECCIONAR SOLO DISCO (Tipo 2 en Gadget) ---
        # Inicio del disco = npart[0] (Gas) + npart[1] (Halo)
        start_disk = npart[0] + npart[1]
        end_disk = start_disk + npart[2]
        
        pos_disk = pos[start_disk:end_disk]
        
        return time, pos_disk

# --- BUCLE PRINCIPAL ---
print(f"Procesando snapshots de {INPUT_DIR}...")

# Buscamos archivos automáticamente
files = sorted([f for f in os.listdir(INPUT_DIR) if f.startswith('snapshot')])

if not files:
    print("¡ERROR! No hay archivos snapshot en la carpeta 'output_B'.")
    print("Asegúrate de que has descargado la carpeta correctamente.")
    exit()

frames_list = []

# 1. GENERAR IMÁGENES
for filename in tqdm(files, desc="Generando imágenes"):
    full_path = os.path.join(INPUT_DIR, filename)
    
    # Leer datos
    try:
        time, pos = read_gadget_snapshot(full_path)
    except:
        continue
    
    if pos is None:
        continue
        
    # --- GENERAR GRÁFICO ---
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Pintamos puntos (Proyección X-Y)
    ax.scatter(pos[:, 0], pos[:, 1], s=0.1, c='cyan', alpha=0.5, marker='.')
    
    # Configuración ejes
    ax.set_xlim(-LIMIT_KPC, LIMIT_KPC)
    ax.set_ylim(-LIMIT_KPC, LIMIT_KPC)
    ax.set_aspect('equal')
    ax.set_xlabel("x (kpc)")
    ax.set_ylabel("y (kpc)")
    
    # Título con tiempo
    ax.set_title(f"Galaxia B - Tiempo: {time:.3f}")
    
    # Guardar imagen
    out_name = os.path.join(OUTPUT_IMG_DIR, filename + ".png")
    plt.savefig(out_name, dpi=100)
    plt.close(fig)
    
    frames_list.append(out_name)

# 2. CREAR VIDEO CON OPENCV
if len(frames_list) > 0:
    print("Generando video AVI...")
    
    # Leemos la primera imagen para saber el tamaño
    first_frame = cv2.imread(frames_list[0])
    height, width, layers = first_frame.shape
    
    # Configuramos el video (10 FPS)
    video = cv2.VideoWriter(VIDEO_NAME, cv2.VideoWriter_fourcc(*'MJPG'), 10, (width, height))

    for image_file in tqdm(frames_list, desc="Montando video"):
        video.write(cv2.imread(image_file))

    cv2.destroyAllWindows()
    video.release()
    
    print(f"\n¡LISTO! Video guardado como: {VIDEO_NAME}")
else:
    print("No se generaron imágenes.")