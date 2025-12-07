import numpy as np
import matplotlib.pyplot as plt
import os
import struct
import glob

# --- CONFIGURACIÓN ---
INPUT_DIR = "output_B"   # Carpeta con los datos
LIMIT_KPC = 15.0         # Límite para el análisis

# --- FUNCIÓN DE LECTURA (La misma de siempre) ---
def read_gadget_snapshot(filename):
    if not os.path.exists(filename): return None, None
    with open(filename, 'rb') as f:
        dummy = struct.unpack('i', f.read(4))[0] 
        if dummy != 256: return None, None
        npart = np.fromfile(f, dtype=np.int32, count=6)
        massarr = np.fromfile(f, dtype=np.float64, count=6)
        time = struct.unpack('d', f.read(8))[0]
        f.seek(256 - 80, 1) 
        dummy = struct.unpack('i', f.read(4))[0]
        dummy = struct.unpack('i', f.read(4))[0]
        n_total = np.sum(npart)
        pos = np.fromfile(f, dtype=np.float32, count=n_total*3).reshape(-1, 3)
        
        # Seleccionar DISCO (Tipo 2)
        start_disk = npart[0] + npart[1]
        end_disk = start_disk + npart[2]
        pos_disk = pos[start_disk:end_disk]
        
        return time, pos_disk

# --- PARTE 1: EXTENSIÓN VS TIEMPO ---
print("Analizando extensión espacial en función del tiempo...")

files = sorted([f for f in os.listdir(INPUT_DIR) if f.startswith('snapshot')])
times = []
std_x = []
std_y = []
std_z = []

# Variables para guardar el último snapshot válido para la Parte 2
last_pos = None
last_time = 0

for filename in files:
    full_path = os.path.join(INPUT_DIR, filename)
    try:
        time, pos = read_gadget_snapshot(full_path)
    except: continue
    
    if pos is None or len(pos) == 0: continue
    
    # Guardamos datos para luego
    times.append(time)
    
    # Calculamos la "extensión" como la desviación estándar de las posiciones
    # Esto nos dice cuán "dispersa" está la galaxia en cada eje
    std_x.append(np.std(pos[:, 0]))
    std_y.append(np.std(pos[:, 1]))
    std_z.append(np.std(pos[:, 2]))
    
    # Guardamos el último para la parte 2
    last_pos = pos
    last_time = time

# Gráfica 1: Extensión vs Tiempo
plt.figure(figsize=(10, 6))
plt.plot(times, std_x, 'b-', label='Extensión Eje X (Radio)')
plt.plot(times, std_y, 'g--', label='Extensión Eje Y (Radio)')
plt.plot(times, std_z, 'r', linewidth=2, label='Extensión Eje Z (Espesor)')

plt.xlabel('Tiempo (Unidades internas)')
plt.ylabel('Desviación Estándar Espacial (kpc)')
plt.title('Evolución del Tamaño de la Galaxia')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('extension_vs_tiempo.png')
print("-> Gráfica guardada: extension_vs_tiempo.png")


# --- PARTE 2: ESCALA VERTICAL VS RADIO (Último Snapshot) ---
print(f"\nAnalizando escala vertical para el último instante (t={last_time:.2f})...")

if last_pos is not None:
    # Coordenadas
    x = last_pos[:, 0]
    y = last_pos[:, 1]
    z = last_pos[:, 2]
    
    # Radio cilíndrico R = sqrt(x^2 + y^2)
    R = np.sqrt(x**2 + y**2)
    
    # Definimos anillos (bins) radiales de 0 a 15 kpc
    bins = np.linspace(0, 15, 30) # 30 anillos
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    
    z_scale_height = []
    
    for i in range(len(bins)-1):
        R_min = bins[i]
        R_max = bins[i+1]
        
        # Seleccionamos partículas en este anillo
        mask = (R >= R_min) & (R < R_max)
        z_in_ring = z[mask]
        
        if len(z_in_ring) > 10:
            # La escala vertical se suele estimar como el RMS de Z (root mean square)
            # o la desviación estándar
            hz = np.std(z_in_ring)
            z_scale_height.append(hz)
        else:
            z_scale_height.append(np.nan)
            
    # Gráfica 2: Escala Vertical vs Radio
    plt.figure(figsize=(10, 6))
    plt.plot(bin_centers, z_scale_height, 'ko-', linewidth=2, label='Espesor del Disco (hz)')
    
    plt.xlabel('Radio Galactocéntrico R (kpc)')
    plt.ylabel('Escala Vertical hz (kpc)')
    plt.title(f'Estructura Vertical del Disco en t={last_time:.2f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('escala_vertical_vs_radio.png')
    print("-> Gráfica guardada: escala_vertical_vs_radio.png")
    
else:
    print("Error: No se encontraron datos para el análisis vertical.")

print("\n¡Análisis completado!")