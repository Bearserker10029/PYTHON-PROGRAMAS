# Algoritmo de Grover para encontrar un elemento en una lista no ordenada
from Q_Lenguaje import *
from math import pi, sqrt, floor
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
from multiprocessing import Process

# Número de qubits
n_qbits = 3
N = 2 ** n_qbits  # Total de estados posibles

# --- Lista de soluciones como cadenas binarias ---
soluciones_binarias = ["100", "001"]  # puedes agregar más
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

# Graficar el estado final en 3D
estados_por_iteracion = [estado_s]
estado_actual = estado_s
for _ in range(iteraciones):
    estado_actual = multiplicar(Us, multiplicar(Uw, estado_actual))
    estados_por_iteracion.append(estado_actual)

# Convertir cada estado a np.array para facilitar reducción por qubit
estados_np = [np.array([x[0] for x in est], dtype=complex) for est in estados_por_iteracion]
def bloch_animacion():
    fig = plt.figure(figsize=(4 * n_qbits, 6))
    axes = [fig.add_subplot(1, n_qbits, i+1, projection='3d') for i in range(n_qbits)]

    # Dibujar esferas de Bloch vacías
    def plot_bloch_sphere(ax):
        u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        ax.plot_surface(x, y, z, color='lightblue', alpha=0.3, linewidth=0)
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
        ax.axis('off')

    for ax in axes:
        plot_bloch_sphere(ax)

    # Inicializar vectores y trayectorias
    vectors = [None] * n_qbits
    trayectorias = [[] for _ in range(n_qbits)]

    # Función de actualización por frame
    def update(frame):
        for i in range(n_qbits):
            ket = reducir_qubit(estados_np[frame], i)
            bloch_vec = ket_to_bloch_vector(ket)

            trayectorias[i].append(bloch_vec)
            if vectors[i] is not None:
                vectors[i].remove()
            trayectoria = np.array(trayectorias[i])
            axes[i].plot3D(trayectoria[:,0], trayectoria[:,1], trayectoria[:,2],
                           color='cyan', linewidth=1.5, alpha=0.6)    
            vectors[i] = axes[i].quiver(0, 0, 0, *bloch_vec, color='red', linewidth=2)
            axes[i].set_title(f'Qubit {i} - Iteración {frame}')
        return vectors

    anim = FuncAnimation(fig, update, frames=len(estados_np), interval=800, blit=False, repeat=False)
    plt.tight_layout()
    plt.show()

# --- Ejecutar ambas visualizaciones en paralelo ---
if __name__ == "__main__":
    p1 = Process(target=graficar, args=(estado_final,))
    p2 = Process(target=bloch_animacion)
    p1.start()
    p2.start()
    p1.join()
    p2.join()