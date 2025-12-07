# Práctica 1: Fotometría y Morfología Galáctica 

Este módulo se centra en el análisis de datos observacionales reales (fotometría) de la galaxia **NGC 628**. El objetivo es caracterizar su estructura morfológica y sus poblaciones estelares mediante el estudio de sus perfiles de brillo y color.

## Scripts Incluidos

### 1. Perfil de Brillo Superficial (`Perfil_brillo.py`)
Genera la visualización de los perfiles de brillo superficial ($\mu$) en función del radio galactocéntrico.
- **Input:** Datos csv con magnitudes en bandas $g, r, i$.
- **Output:** Gráfica comparativa de las bandas, permitiendo identificar la estructura del disco.

### 2. Cálculo de la Longitud de Escala (`H_r.py`)
Determina el parámetro de escala ($H_r$) del disco galáctico asumiendo un perfil exponencial:
$$I(R) = I_0 e^{-R/H_r} \quad \rightarrow \quad \mu(R) = \mu_0 + 1.0857 \frac{R}{H_r}$$
- Realiza un ajuste lineal robusto en la región del disco.
- Calcula la propagación de errores para obtener la incertidumbre de $H_r$ en kpc.

### 3. Gradientes de Color (`diagramag_r.py`)
Analiza la distribución del índice de color ($g - r$) a lo largo del radio.
- Permite inferir la edad de las poblaciones estelares (zonas azules vs rojas) y la metalicidad.
- Aplica suavizado de datos (rolling average) para reducir el ruido observacional.

---
*Datos utilizados: Fotometría superficial de NGC 628.*
