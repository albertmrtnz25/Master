# Cosmology Coursework 

Aquí he recopilado los scripts y herramientas computacionales que desarrollé para la asignatura de **Cosmología**. 

Más allá de resolver las ecuaciones en papel, mi objetivo era construir pequeñas herramientas de simulación para visualizar cómo se comporta el universo bajo diferentes modelos teóricos.

##  Contenido del Repositorio

### 1. Modelos de Expansión del Universo (`universe_expansion.py`)
¿Cómo cambia la edad y el tamaño del universo si modificamos su composición? 
Este script compara tres escenarios clásicos resolviendo las **Ecuaciones de Friedmann**:
* **Lambda-CDM:** El modelo de concordancia actual (Materia + Energía Oscura).
* **Einstein-de Sitter:** Un universo dominado solo por materia (plano).
* **Universo de Milne:** Un modelo de universo vacío (curvatura negativa).

> **Lo interesante:** El código está estructurado con **Clases y Polimorfismo**, lo que permite añadir nuevos modelos cosmológicos (ej. con radiación) simplemente heredando de la clase base.

### 2. Integración Numérica con Bessel (`bessel_integration.py`)
En cosmología (especialmente en el universo temprano y termodinámica de reliquias), a menudo aparecen integrales que no tienen solución analítica.
Este script resuelve numéricamente una integral que involucra el cociente de **Funciones de Bessel Modificadas ($K_1/K_2$)**, analizando su convergencia asintótica mediante `scipy.integrate`.
