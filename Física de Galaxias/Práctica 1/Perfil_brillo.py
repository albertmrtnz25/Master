import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Tuple
from io import StringIO

class GalaxyProfilePlotter:
    """
    Clase para visualizar y analizar perfiles de brillo superficial de galaxias.
    Realiza ajustes lineales automáticos en regiones específicas del perfil.
    """

    def __init__(self, data: pd.DataFrame, sma_col: str = 'SMA'):
        """
        Args:
            data (pd.DataFrame): DataFrame con los datos de fotometría.
            sma_col (str): Nombre de la columna del eje semi-mayor.
        """
        self.df = data.sort_values(sma_col).reset_index(drop=True)
        self.sma_col = sma_col
        self.fit_results = {} # Almacenará los coeficientes del ajuste

    def get_available_bands(self) -> List[str]:
        """Detecta automáticamente las columnas de magnitud (empiezan por 'mu_')."""
        return [col.replace('mu_', '') for col in self.df.columns if col.startswith('mu_')]

    def fit_profiles(self, 
                     lower_frac: float = 0.03, 
                     upper_frac: float = 0.80) -> Dict[str, np.ndarray]:
        """
        Realiza un ajuste lineal (y = mx + b) en el rango especificado.
        
        Args:
            lower_frac (float): Límite inferior (fracción del radio total).
            upper_frac (float): Límite superior (fracción del radio total).
        """
        bands = self.get_available_bands()
        x = self.df[self.sma_col].values
        
        # Definir rango dinámico en base a los datos
        x_min, x_max = x.min(), x.max()
        x_low_limit = x_min + lower_frac * (x_max - x_min)
        x_high_limit = x_min + upper_frac * (x_max - x_min)
        
        # Máscara booleana para seleccionar la región de interés
        mask = (x >= x_low_limit) & (x <= x_high_limit)
        
        # Guardamos los límites para usarlos en la gráfica
        self.fit_bounds = (x_low_limit, x_high_limit)

        print(f"--- Ajustando perfiles entre {x_low_limit:.2f} y {x_high_limit:.2f} arcsec ---")

        for band in bands:
            col_name = f'mu_{band}'
            y = self.df[col_name].values
            
            # Ajuste polinómico de grado 1 (Lineal)
            # coef[0] = pendiente, coef[1] = ordenada
            coef = np.polyfit(x[mask], y[mask], 1)
            self.fit_results[band] = coef
            
            print(f"Banda {band}: Pendiente={coef[0]:.4f}, Intercepto={coef[1]:.2f}")
            
        return self.fit_results

    def plot_profiles(self, 
                      save_path: Optional[str] = None, 
                      title: str = "Perfil de Brillo Superficial"):
        """Genera la visualización final con datos y ajustes."""
        
        if not self.fit_results:
            print("Advertencia: Ejecuta 'fit_profiles' antes de graficar para ver las líneas de tendencia.")

        plt.figure(figsize=(10, 7), dpi=120)
        plt.style.use('seaborn-v0_8-whitegrid') # Estilo profesional
        
        # Configuración estética por banda (extensible)
        styles = {
            'r': {'color': '#e74c3c', 'marker': 'D', 'label': 'Banda r'},
            'g': {'color': '#27ae60', 'marker': 'o', 'label': 'Banda g'},
            'i': {'color': '#2980b9', 'marker': '^', 'label': 'Banda i'}
        }
        
        x = self.df[self.sma_col]

        # 1. Graficar Datos Crudos
        for band in self.get_available_bands():
            style = styles.get(band, {'color': 'gray', 'marker': 'x', 'label': band})
            y = self.df[f'mu_{band}']
            
            plt.scatter(x, y, label=style['label'], color=style['color'], 
                        marker=style['marker'], s=40, alpha=0.8, edgecolors='white')

            # 2. Graficar Líneas de Ajuste (si existen)
            if band in self.fit_results:
                slope, intercept = self.fit_results[band]
                
                # Crear línea solo en el rango de ajuste
                low, high = self.fit_bounds
                x_fit = np.linspace(low, high, 100)
                y_fit = slope * x_fit + intercept
                
                plt.plot(x_fit, y_fit, color=style['color'], linestyle='-', linewidth=2, alpha=0.9)

        # 3. Decoración de la Gráfica
        if hasattr(self, 'fit_bounds'):
            plt.axvline(self.fit_bounds[0], color='black', linestyle='--', alpha=0.5, linewidth=1)
            plt.axvline(self.fit_bounds[1], color='black', linestyle='--', alpha=0.5, linewidth=1)
            plt.text(self.fit_bounds[0], plt.ylim()[0], ' Inicio Ajuste', rotation=90, verticalalignment='bottom')

        plt.gca().invert_yaxis() # Magnitudes astronómicas
        plt.xlabel('Radio (SMA) [arcsec]', fontsize=12)
        plt.ylabel(r'Brillo Superficial $\mu$ [mag/arcsec$^2$]', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            print(f"Gráfica guardada en: {save_path}")
        plt.show()

# --- Mock Data para probar el código (Copiar y Pegar) ---
RAW_CSV = """SMA,mu_r,mu_g,mu_i
0.00,17.52,18.54,16.97
1.98,18.42,19.13,18.03
7.92,19.36,19.95,18.89
13.86,19.89,20.63,19.17
19.80,20.29,21.01,19.83
25.74,20.49,21.23,20.04
31.68,20.72,21.42,20.32
37.62,20.79,21.53,20.45
43.56,20.90,21.56,20.55
49.50,21.01,21.60,20.65
55.44,21.17,21.72,20.78
61.38,20.78,21.39,20.62
67.32,21.23,21.90,20.66
73.26,21.17,21.87,20.69
79.20,21.45,22.14,21.16
85.14,21.54,22.17,21.28
91.08,21.62,22.21,21.30
97.02,21.68,22.24,21.38
102.96,21.78,22.09,21.55
108.90,21.59,22.22,21.56
114.84,21.90,22.27,21.70
120.78,22.06,22.48,21.78
126.72,22.07,22.58,21.89
132.66,22.21,22.63,21.99
138.60,22.42,22.78,22.14
144.54,22.48,22.98,22.24
150.48,22.48,22.92,22.33
"""

if __name__ == "__main__":
    # Cargar datos
    df = pd.read_csv(StringIO(RAW_CSV))
    
    # Instanciar el visualizador
    plotter = GalaxyProfilePlotter(data=df)
    
    # 1. Realizar el ajuste (Podemos cambiar los rangos aquí fácilmente)
    plotter.fit_profiles(lower_frac=0.05, upper_frac=0.85)
    
    # 2. Generar la gráfica final
    plotter.plot_profiles(save_path='perfil_ngc628.png', title='Análisis de Perfil: NGC 628')