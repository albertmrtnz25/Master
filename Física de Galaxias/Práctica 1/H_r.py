import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from io import StringIO
from typing import Dict, List, Optional, Tuple

# Constantes Físicas y de Conversión
# Factor de conversión de magnitudes a flujo lineal: 2.5 * log10(e)
POGSON_SCALE_FACTOR = 2.5 * np.log10(np.e) 

class GalaxyMorphologyFitter:
    """
    Herramienta para ajustar perfiles de brillo superficial de galaxias 
    y determinar longitudes de escala (Scale Lengths) en discos exponenciales.
    """

    def __init__(self, data: pd.DataFrame, pixel_scale_kpc: float):
        """
        Args:
            data (pd.DataFrame): DataFrame con columnas 'r_arcsec', 'mu_r', 'mu_g', 'mu_i'.
            pixel_scale_kpc (float): Factor de conversión arcsec -> kpc para la distancia de la galaxia.
        """
        self.df = data
        self.scale_kpc = pixel_scale_kpc
        self.results = {}

    @staticmethod
    def _linear_model(r: float, mu0: float, slope: float) -> float:
        """Modelo lineal: mu(r) = mu0 + slope * r"""
        return mu0 + slope * r

    def fit_exponential_disk(self, bands: List[str] = ['r', 'g', 'i']) -> pd.DataFrame:
        """
        Realiza el ajuste para las bandas especificadas y calcula H_r.
        """
        fit_summary = []

        for band in bands:
            col_name = f'mu_{band}'
            if col_name not in self.df.columns:
                print(f"Advertencia: Banda {band} no encontrada en los datos.")
                continue

            # 1. Limpieza de datos (Drop NaNs)
            valid_data = self.df[['r_arcsec', col_name]].dropna()
            r_vals = valid_data['r_arcsec'].values
            mu_vals = valid_data[col_name].values

            if len(r_vals) < 3:
                continue # No hay suficientes puntos para ajustar

            # 2. Ajuste (Curve Fit)
            # Slope (m) = 1.0857 / H_r  -> H_r = 1.0857 / m
            popt, pcov = curve_fit(self._linear_model, r_vals, mu_vals, p0=[20, 0.1])
            
            mu0, slope = popt
            perr = np.sqrt(np.diag(pcov))
            err_mu0, err_slope = perr

            # 3. Cálculo de H_r y Propagación de Errores
            # H_r = C / slope
            # Error(H_r) = | -C / slope^2 | * error_slope
            h_r_arcsec = POGSON_SCALE_FACTOR / slope
            h_r_error_arcsec = (POGSON_SCALE_FACTOR / (slope**2)) * err_slope

            # 4. Conversión a Kpc
            h_r_kpc = h_r_arcsec * self.scale_kpc
            h_r_error_kpc = h_r_error_arcsec * self.scale_kpc

            # Guardamos resultados estructurados
            fit_summary.append({
                'Band': band,
                'H_r (arcsec)': h_r_arcsec,
                'err_H_r (arcsec)': h_r_error_arcsec,
                'H_r (kpc)': h_r_kpc,
                'err_H_r (kpc)': h_r_error_kpc,
                'mu_0': mu0,
                'err_mu_0': err_mu0,
                'slope': slope
            })
            
            # Guardamos parámetros internos para plotear después
            self.results[band] = {'popt': popt, 'r_vals': r_vals, 'mu_vals': mu_vals}

        return pd.DataFrame(fit_summary)

    def plot_fits(self, save_path: Optional[str] = None):
        """Genera una visualización de los datos y los ajustes."""
        if not self.results:
            print("No hay ajustes para graficar. Ejecuta fit_exponential_disk primero.")
            return

        plt.figure(figsize=(10, 6), dpi=100)
        plt.style.use('seaborn-v0_8-whitegrid')
        
        colors = {'r': '#e74c3c', 'g': '#27ae60', 'i': '#2980b9'}

        for band, data in self.results.items():
            # Datos crudos
            plt.scatter(data['r_vals'], data['mu_vals'], label=f'Banda {band} (Obs)', 
                        color=colors.get(band, 'black'), s=15, alpha=0.7)
            
            # Línea de ajuste
            mu0, slope = data['popt']
            r_range = np.linspace(min(data['r_vals']), max(data['r_vals']), 100)
            plt.plot(r_range, self._linear_model(r_range, mu0, slope), 
                     linestyle='--', color=colors.get(band, 'black'), linewidth=1.5)

        plt.gca().invert_yaxis() # Magnitudes: mayor valor es menos brillo
        plt.xlabel('Radio (arcsec)')
        plt.ylabel(r'Brillo Superficial $\mu$ (mag/arcsec$^2$)')
        plt.title('Ajuste de Disco Exponencial (Perfil Radial)')
        plt.legend()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()

    @staticmethod
    def generate_latex_table(df_results: pd.DataFrame) -> str:
        """Genera el código LaTeX listo para copiar/pegar en Overleaf."""
        header = r"""
\begin{table}[h!]
    \centering
    \caption{Resultados del ajuste exponencial.}
    \begin{tabular}{lccc}
        \toprule
        \textbf{Banda} & \textbf{$H_r$ (arcsec)} & \textbf{$H_r$ (kpc)} & \textbf{$\mu_0$} \\
        \midrule
"""
        body = ""
        for _, row in df_results.iterrows():
            body += f"        {row['Band']} & ${row['H_r (arcsec)']:.2f} \\pm {row['err_H_r (arcsec)']:.2f}$ & "
            body += f"${row['H_r (kpc)']:.2f} \\pm {row['err_H_r (kpc)']:.2f}$ & "
            body += f"${row['mu_0']:.2f} \\pm {row['err_mu_0']:.2f}$ \\\\\n"

        footer = r"""        \bottomrule
    \end{tabular}
\end{table}
"""
        return header + body + footer

# --- Datos de Ejemplo (Mock Data) ---
# En producción, esto se lee de un archivo externo
RAW_DATA = """
r_arcsec,mu_r,mu_g,mu_i
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

# --- Ejecución Principal ---
if __name__ == "__main__":
    # Cargar datos
    df_galaxy = pd.read_csv(StringIO(RAW_DATA))
    
    # 1. Instanciar la herramienta con la física de la galaxia (escala)
    fitter = GalaxyMorphologyFitter(data=df_galaxy, pixel_scale_kpc=0.0465)
    
    # 2. Realizar el ajuste
    results_df = fitter.fit_exponential_disk()
    
    # 3. Mostrar resultados en consola (como tabla limpia de Pandas)
    print("Resultados del Ajuste:")
    print(results_df[['Band', 'H_r (kpc)', 'err_H_r (kpc)']])
    
    # 4. Generar LaTeX
    print("\n--- Código LaTeX ---")
    print(GalaxyMorphologyFitter.generate_latex_table(results_df))
    
    # 5. Visualizar
    fitter.plot_fits()