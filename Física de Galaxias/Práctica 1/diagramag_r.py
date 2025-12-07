import pandas as pd
import matplotlib.pyplot as plt
import io
from typing import Optional

class GalaxyPhotometryAnalyzer:
    """
    Analizador de perfiles fotométricos de galaxias.
    Procesa datos de brillo superficial para obtener gradientes de color y metalicidad.
    """

    def __init__(self, raw_data: str):
        """
        Inicializa el analizador cargando los datos crudos.
        
        Args:
            raw_data (str): String en formato CSV con columnas SMA, mu_r, mu_g, mu_i.
        """
        try:
            self.df = pd.read_csv(io.StringIO(raw_data))
            self._validate_data()
        except Exception as e:
            raise ValueError(f"Error al procesar los datos de entrada: {e}")

    def _validate_data(self):
        """Asegura que las columnas necesarias existan."""
        required_cols = ['SMA', 'mu_g', 'mu_r']
        if not all(col in self.df.columns for col in required_cols):
            raise ValueError(f"Faltan columnas requeridas. Se necesitan: {required_cols}")

    def compute_color_indices(self) -> pd.DataFrame:
        """
        Calcula el índice de color (g - r).
        El color es un indicador de la población estelar (vieja/roja vs joven/azul).
        """
        # Vectorización con Pandas (rápido y eficiente)
        self.df['g_r'] = self.df['mu_g'] - self.df['mu_r']
        
        # Añadimos una media móvil (rolling mean) para suavizar el ruido observacional
        # Esto es muy común en análisis de series temporales o datos espaciales
        self.df['g_r_smooth'] = self.df['g_r'].rolling(window=3, center=True).mean()
        
        return self.df

    def plot_color_profile(self, save_path: Optional[str] = None):
        """
        Genera una visualización profesional del perfil de color radial.
        """
        if 'g_r' not in self.df.columns:
            self.compute_color_indices()

        plt.figure(figsize=(10, 6), dpi=100)
        plt.style.use('seaborn-v0_8-whitegrid')

        # 1. Datos crudos (puntos dispersos)
        plt.plot(self.df['SMA'], self.df['g_r'], 'o', 
                 color='#bdc3c7', alpha=0.6, label='Datos Observados', markersize=4)

        # 2. Tendencia suavizada (Línea sólida)
        # Usamos la versión suavizada si hay suficientes datos, si no, la original
        y_trend = self.df['g_r_smooth'] if not self.df['g_r_smooth'].isna().all() else self.df['g_r']
        
        plt.plot(self.df['SMA'], y_trend, 
                 color='#c0392b', linewidth=2.5, label='Tendencia (Suavizada)')

        # Estética científica
        plt.xlabel(r'Radio (Semi-Major Axis) [arcsec]', fontsize=12)
        plt.ylabel(r'Índice de Color $g - r$ [mag]', fontsize=12)
        plt.title('Perfil Radial de Color: Gradiente de Población Estelar', fontsize=14)
        
        # Anotaciones físicas (interpretación de los datos)
        # Detectamos si el centro es más rojo o azul
        center_color = self.df['g_r'].iloc[0]
        outer_color = self.df['g_r'].iloc[-1]
        
        if center_color < outer_color:
            trend_text = "Tendencia: Enrojecimiento hacia fuera (Outside-in?)"
        else:
            trend_text = "Tendencia: Centro rojo (Bulbo clásico)"
            
        plt.annotate(trend_text, xy=(0.05, 0.95), xycoords='axes fraction', 
                     fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.7)
        
        if save_path:
            plt.savefig(save_path)
            print(f"Gráfica guardada en {save_path}")
        else:
            plt.show()

# --- Simulación de carga de datos (Data Mocking) ---
# En un entorno real, esto vendría de un archivo 'galaxy_data.csv'
RAW_CSV_DATA = """SMA,mu_r,mu_g,mu_i
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
    # Flujo de trabajo típico de Data Science
    print("Iniciando análisis fotométrico...")
    
    analyzer = GalaxyPhotometryAnalyzer(RAW_CSV_DATA)
    analyzer.compute_color_indices()
    
    # Visualización
    analyzer.plot_color_profile()