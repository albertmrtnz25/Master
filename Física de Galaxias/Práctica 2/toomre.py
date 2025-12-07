import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 1. Cargar datos
try:
    data = np.loadtxt('toomre.dat')
except:
    print("Error: No encuentro toomre.dat")
    exit()

R = data[:, 0]
Q = data[:, 1]

# 2. Graficar
plt.figure(figsize=(10, 6))

plt.plot(R, Q, 'k-', linewidth=2, label='Parámetro Q de Toomre')

# Dibujamos la linea critica de estabilidad Q=1
plt.axhline(y=1.0, color='r', linestyle='--', linewidth=2, label='Límite de Estabilidad (Q=1)')

# Decoracion
plt.xlabel('Radio (kpc)')
plt.ylabel('Parámetro de Toomre Q')
plt.title('Estabilidad del Disco (Galaxia B)')
plt.legend()
plt.grid(True, alpha=0.3)

# Ajustamos los ejes para ver bien la zona crítica
plt.xlim(0, 6.5) # Los datos parecen llegar hasta 6 kpc
plt.ylim(0, 5)   # Limitamos Y para ver bien el cruce por 1

# Guardar
plt.savefig('parametro_toomre.png')
print("Gráfica guardada como 'parametro_toomre.png'")