import numpy as np
from scipy.integrate import quad
from scipy.special import kv
import math
import matplotlib.pyplot as plt

def frac_K1_K2(y): #fraccion de funciones de bessel

    return kv(1,y)/kv(2,y)

def integrando(y): #definimos el integrando

    r = frac_K1_K2(y)
    return (y**2.5) * math.exp(-y) * r

def I_x(x): #calculamos la integral empleando quad
    if x <= 0:
        return 0.0
    val, err = quad(integrando, 0.0, x)
    return val

# compute values
xs = np.linspace(0, 50, 1000)
vals = [I_x(float(x)) for x in xs]
for x in xs:
    print(f"I({x}) = {I_x(x)}")
    
x10 = xs[xs>10] #vemos que para x>10 se empieza a estabilizar
lx10 = len(x10) #longitud array
suma = 0

for x in x10:
    intg = I_x(x)
    suma = suma + intg
media = suma/lx10
print("Valor medio I(x>>1) = ", media)

# plot
plt.figure(figsize=(6,4))
plt.plot(xs, vals, label='I(x)')
plt.axhline(y=media, color='r', linestyle = '--', label = 'Valor medio para x>>1')
plt.xlabel("x")
plt.ylabel("I(x)")
plt.title("Integral I(x)")
plt.legend()
plt.tight_layout()
plt.show()

