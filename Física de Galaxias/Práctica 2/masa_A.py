import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE UNIDADES ---
# Factor para convertir la velocidad interna a km/s.
# Basado en tus datos (V~0.7 en R=8), un factor de 300 da V~210 km/s (realista).
UNIT_VELOCITY = 300.0 
G_CONST = 4.301e-6  # Constante G en (kpc * km^2/s^2 / M_sol)

# 1. Cargar datos
try:
    data = np.loadtxt('freqdbh.dat')
except:
    print("Error: No encuentro freqdbh.dat")
    exit()

# 2. Leer columnas (El archivo está en unidades internas)
R_kpc = data[:, 0]          # Asumimos que el radio ya está en kpc (0 a 25)
Omega_halo = data[:, 1]     
V_total_code = data[:, 4]   # Velocidad en unidades de código
V_bulbo_code = data[:, 5]   # Velocidad en unidades de código

# 3. CONVERSIÓN A UNIDADES FÍSICAS
V_total = V_total_code * UNIT_VELOCITY
V_bulbo = V_bulbo_code * UNIT_VELOCITY

# Recalculamos Halo y Disco usando las velocidades físicas
# V_halo = R * Omega. Ojo: Omega también necesita escalado si R está en kpc.
# Método más seguro: Calcular V_halo restando componentes si tenemos dudas de Omega,
# PERO el archivo da Omega. Asumamos que V_halo_code = R * Omega_code
V_halo_code = R_kpc * Omega_halo
V_halo = V_halo_code * UNIT_VELOCITY

# V_disco por descarte: V_tot^2 = V_b^2 + V_d^2 + V_h^2
V_disco_sq = V_total**2 - V_bulbo**2 - V_halo**2
V_disco = np.sqrt(np.maximum(V_disco_sq, 0))

# 4. CALCULO DE MASA ACUMULATIVA M(<R)
# Formula: M = (R * V^2) / G
# Evitamos división por cero usando np.where o máscara
M_total = np.zeros_like(R_kpc)
M_bulbo = np.zeros_like(R_kpc)
M_halo = np.zeros_like(R_kpc)
M_disco = np.zeros_like(R_kpc)

# Calculamos solo donde R > 0 para evitar errores
mask = R_kpc > 0
M_total[mask] = (R_kpc[mask] * V_total[mask]**2) / G_CONST
M_bulbo[mask] = (R_kpc[mask] * V_bulbo[mask]**2) / G_CONST
M_halo[mask]  = (R_kpc[mask] * V_halo[mask]**2)  / G_CONST
M_disco[mask] = (R_kpc[mask] * V_disco[mask]**2) / G_CONST

# 5. GRAFICAR
plt.figure(figsize=(10, 6))

# Escala Y en 10^10 Masas solares
scale = 1e10

plt.plot(R_kpc, M_total/scale, 'k-', linewidth=2, label='Masa Total Dinámica')
plt.plot(R_kpc, M_disco/scale, 'g--', linewidth=2, label='Masa Disco')
plt.plot(R_kpc, M_halo/scale,  'r:', linewidth=2, label='Masa Halo')
plt.plot(R_kpc, M_bulbo/scale, 'b-.', linewidth=2, label='Masa Bulbo')

plt.xlabel('Radio (kpc)')
plt.ylabel(r'Masa Acumulada ($10^{10} M_{\odot}$)')
plt.title('Distribución de Masa Acumulativa (Unidades Corregidas)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 15)
plt.ylim(0, None) # Dejar que matplotlib ajuste el límite superior

plt.savefig('masa_acumulativa_corregida.png')
print("Gráfica guardada: masa_acumulativa_corregida.png")