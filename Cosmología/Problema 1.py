import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List

# --- Configuración Global y Constantes ---
# Usamos dataclass o constantes simples para configuración
H_PARAM = 0.674  # Parámetro de Hubble reducido h
H0 = 100 * H_PARAM 
T_HUBBLE_INV = 1.0  # Trabajaremos en unidades de tiempo de Hubble (1/H0)

class CosmologicalModel(ABC):
    """
    Clase abstracta que define la interfaz para cualquier modelo de universo FLRW.
    Obliga a que todos los modelos tengan un nombre y una forma de calcular el tiempo.
    """
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    @abstractmethod
    def calculate_time(self, a_array: np.ndarray) -> np.ndarray:
        """Calcula el tiempo cósmico t para un array de factores de escala a."""
        pass

    @property
    @abstractmethod
    def age_of_universe(self) -> float:
        """Devuelve la edad del universo t0 (cuando a=1)."""
        pass

class MatterDominatedUniverse(CosmologicalModel):
    """Modelo Einstein-de Sitter (Plano, solo Materia): Omega_M=1."""
    
    def calculate_time(self, a_array: np.ndarray) -> np.ndarray:
        # Solución analítica: t ~ a^(3/2)
        # Inversa de a ~ t^(2/3)
        return (2/3) * (a_array**(3/2))

    @property
    def age_of_universe(self) -> float:
        return 2/3  # En unidades de Hubble

class EmptyUniverse(CosmologicalModel):
    """Modelo de Milne (Vacío): Omega_M=0, Omega_L=0."""
    
    def calculate_time(self, a_array: np.ndarray) -> np.ndarray:
        # Solución analítica lineal: a ~ t
        return a_array 

    @property
    def age_of_universe(self) -> float:
        return 1.0

class LambdaCDMUniverse(CosmologicalModel):
    """Modelo de Concordancia (Materia + Energía Oscura)."""
    
    def __init__(self, omega_m: float = 0.3, omega_l: float = 0.7):
        super().__init__(name=f'Lambda-CDM ($\Omega_M={omega_m}, \Omega_\Lambda={omega_l}$)', color='blue')
        self.omega_m = omega_m
        self.omega_l = omega_l

    def _friedmann_integrand(self, x: float) -> float:
        """Integrando de la ecuación de Friedmann."""
        if x == 0: return 0
        return 1.0 / np.sqrt(self.omega_m / x + self.omega_l * x**2)

    def calculate_time(self, a_array: np.ndarray) -> np.ndarray:
        t_values = np.zeros_like(a_array)
        for i, a in enumerate(a_array):
            # Integramos numéricamente para cada punto del factor de escala
            res, _ = quad(self._friedmann_integrand, 0, a)
            t_values[i] = res
        return t_values

    @property
    def age_of_universe(self) -> float:
        # Calculamos el tiempo para a=1.0
        res, _ = quad(self._friedmann_integrand, 0, 1.0)
        return res

def plot_universe_expansion(models: List[CosmologicalModel], save_path: Optional[str] = None):
    """
    Genera la comparativa visual de la expansión.
    """
    a_range = np.linspace(0.01, 2.5, 300) # Factor de escala de 0 a 2.5
    
    plt.figure(figsize=(10, 7), dpi=100)
    plt.style.use('seaborn-v0_8-whitegrid')

    # Graficamos cada modelo
    for model in models:
        t_vals = model.calculate_time(a_range)
        t_age = model.age_of_universe
        
        plt.plot(t_vals, a_range, label=model.name, color=model.color, linewidth=2.5)
        
        # Marcador de la edad actual
        plt.plot(t_age, 1.0, 'o', color=model.color, markersize=8, markeredgecolor='white')
        
        # Anotación opcional para el LambdaCDM (el más relevante)
        if isinstance(model, LambdaCDMUniverse):
            plt.axvline(t_age, color=model.color, linestyle=':', alpha=0.6)
            plt.text(t_age + 0.05, 0.1, f'Edad Hoy: {t_age:.2f} $1/H_0$', color=model.color, fontweight='bold')

    # Línea de referencia "Hoy" (a=1)
    plt.axhline(1.0, color='gray', linestyle='--', alpha=0.5, label='Actualidad ($a=1$)')

    plt.title(r'Historia de la Expansión Cósmica: Modelos FLRW', fontsize=16)
    plt.xlabel(r'Tiempo Cósmico [$H_0^{-1}$]', fontsize=12)
    plt.ylabel(r'Factor de Escala $a(t)$', fontsize=12)
    plt.xlim(0, 2.0)
    plt.ylim(0, 2.5)
    plt.legend(fontsize=10, loc='upper left')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

# --- Bloque Principal ---
if __name__ == "__main__":
    # Instanciamos los modelos que queremos comparar
    # Esto demuestra escalabilidad: ¡es muy fácil añadir más!
    mis_universos = [
        MatterDominatedUniverse(name=r'Materia Pura ($\Omega_M=1$)', color='#e74c3c'),
        LambdaCDMUniverse(omega_m=0.3, omega_l=0.7),
        EmptyUniverse(name=r'Universo Vacío (Milne)', color='#27ae60')
    ]
    
    print("Calculando evolución de los modelos cosmológicos...")
    plot_universe_expansion(mis_universos)