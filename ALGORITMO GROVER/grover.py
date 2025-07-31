from Q_Lenguaje import *
from math import pi, sqrt, floor
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Algoritmo de Grover para encontrar un elemento en una lista no ordenada

# Número de qubits
n_qbits = 3
N = 2 ** n_qbits  # Total de estados posibles

# --- Lista de soluciones como cadenas binarias ---
soluciones_binarias = ["100","101"]  # puedes agregar más
estados_marcados = [construir_ket(b) for b in soluciones_binarias]
M = len(estados_marcados)                 # Número de soluciones marcadas (puedes ajustar si hay más)

# Estado uniforme |s> = h⊗h⊗h |000>
estado_s = tensorial(h(ket0), tensorial(h(ket0), h(ket0)))
# ver(estado_s)

# Identidad en espacio de n_qbits
I_n = I
for _ in range(n_qbits - 1):
    I_n = tensorial(I, I_n)
# ver(I_n)

# Construir el oráculo Uw
Uw = construir_oraculo(estados_marcados, I_n)
# ver(Uw)

# Difusor Us para n_qbits
Us=groverUs(n_qbits)
# ver(Us)

# algoritmo de Grover
# |q> = Us * Uw * |s>
# Función para aplicar iteraciones de Grover

def aplicarGrover(estado_inicial, Us, Uw, iteraciones):
    estado = estado_inicial
    for _ in range(iteraciones):
        estado = multiplicar(Us, multiplicar(Uw, estado))
    return estado

# Ejecutar algoritmo con N iteraciones
# Número de iteraciones de Grover
iteraciones = floor((pi / 4) * sqrt(N / M))

estado_final = aplicarGrover(estado_s, Us, Uw, iteraciones)

# Medición del estado final
resultados = medirEnsamble(estado_final, 1000)
ver(resultados)
graficar(estado_final)

estado_np = np.array([x[0] for x in estado_final], dtype=complex)

fig = plt.figure(figsize=(12, 4))

for i in range(n_qbits):
    ax = fig.add_subplot(1, n_qbits, i+1, projection='3d')
    qubit_ket = reducir_qubit(estado_np, i)
    plot_bloch(qubit_ket, ax)
    ax.set_title(f'Qubit {i}')

plt.tight_layout()
plt.show()