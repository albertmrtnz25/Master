# Práctica 2: Dinámica Galáctica y Simulaciones N-Cuerpos 

Este módulo combina la física teórica con simulaciones numéricas para estudiar la estabilidad, evolución y composición (Materia Oscura) de las galaxias. Se procesan "snapshots" binarios de simulaciones **Gadget-2**.

##  Scripts Incluidos

### 1. Análisis de Materia Oscura (`curva_rot.py`)
Descomposición de la curva de rotación galáctica para evidenciar la existencia de Materia Oscura.
- Separa la contribución dinámica de: **Bulbo, Disco y Halo**.
- Demuestra que la materia visible no es suficiente para explicar la velocidad de rotación en los bordes ($V_{obs} > V_{baryonic}$).

### 2. Estabilidad Gravitacional (`toomre.py`)
Diagnóstico de la estabilidad local del disco mediante el **Criterio Q de Toomre**:
$$Q = \frac{\kappa \sigma}{3.36 G \Sigma}$$
- Identifica regiones inestables ($Q < 1$) propensas al colapso gravitatorio y formación estelar.
- Visualiza las zonas de riesgo mediante regiones sombreadas.

### 3. Pipeline de Visualización (`Video.py` / `videoZX.py`)
Herramienta optimizada para renderizar la evolución temporal de la simulación.
- **Lectura Binaria:** Procesa archivos nativos de Gadget-2 (structs de C).
- **Renderizado:** Genera mapas de densidad de partículas en proyecciones XY (Face-on) y ZX (Edge-on).
- **Video:** Compila los frames en una animación `.avi` usando OpenCV.

### 4. Evolución Estructural (`analisis_final.py`)
Analiza cómo cambian las propiedades geométricas de la galaxia con el tiempo.
- Calcula la **escala de altura vertical ($h_z$)**.
- Monitoriza la dispersión de velocidades y la extensión radial.


---
*Simulaciones: Ejecutadas con código SPH Gadget-2.*
