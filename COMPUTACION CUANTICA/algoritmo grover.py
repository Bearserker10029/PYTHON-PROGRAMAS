# Algoritmo de Grover para encontrar un elemento en una lista no ordenada
from Q_Lenguaje import *
from math import pi, sqrt, floor
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
from multiprocessing import Process

# Número de qubits
n_qubits = int(input("Ingrese número de qubits: "))
N = 2 ** n_qubits  # Total de estados posibles

# --- Lista de soluciones como cadenas binarias ---

soluciones_binarias = list()  # puedes agregar más

print(f"Ingrese soluciones entre 0 y {N - 1} (una por línea). Escriba 'fin' para terminar:")

while True:
    entrada = input("> ").strip()
    if entrada.lower() == "fin":
        break
    if not entrada.isdigit():
        print("❌ Entrada inválida. Debe ser un número entero.")
        continue
    valor = int(entrada)
    if not (0 <= valor < N):
        print(f"❌ Fuera de rango. Debe estar entre 0 y {N - 1}.")
        continue
    binario = format(valor, f"0{n_qubits}b")  # Binario con ceros a la izquierda
    soluciones_binarias.append(binario)

# Mostrar las soluciones ingresadas
print(f"✅ Soluciones ingresadas: {soluciones_binarias}")


estados_marcados = [construir_ket(b) for b in soluciones_binarias]
M = len(estados_marcados)                 # Número de soluciones marcadas (puedes ajustar si hay más)

# Estado uniforme |s> = h⊗h⊗h |000>
estado_s = h(ket0)
for _ in range(n_qubits - 1):
    estado_s = tensorial(h(ket0), estado_s)
# ver(estado_s)

# Identidad en espacio de n_qubits
I_n = I
for _ in range(n_qubits - 1):
    I_n = tensorial(I, I_n)
# ver(I_n)

# Construir el oráculo Uw
Uw = construir_oraculo(estados_marcados, I_n)
# ver(Uw)

# Difusor Us para n_qubits
Us=groverUs(n_qubits)
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
    fig = plt.figure(figsize=(4 * n_qubits, 6))
    axes = [fig.add_subplot(1, n_qubits, i+1, projection='3d') for i in range(n_qubits)]
    # Dibujar esferas de Bloch vacías
    def plot_bloch_sphere(ax):
        u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)

        # Esfera de Bloch
        ax.plot_surface(x, y, z, color='lightblue', alpha=0.3, linewidth=0)
        
        # Malla sobre la esfera
        ax.plot_wireframe(x, y, z, color='gray', linewidth=0.3, alpha=0.4)

        # Ejes X, Y, Z
        ax.quiver(0, 0, 0, 1, 0, 0, color='green', linewidth=1.5)  # X
        ax.quiver(0, 0, 0, 0, 1, 0, color='blue', linewidth=1.5)   # Y
        ax.quiver(0, 0, 0, 0, 0, 1, color='black', linewidth=1.5)  # Z

        # Líneas de referencia (trayectoria ejes)
        ax.plot([0, 1], [0, 0], [0, 0], linestyle='--', color='green', alpha=0.6)
        ax.plot([0, 0], [0, 1], [0, 0], linestyle='--', color='blue', alpha=0.6)
        ax.plot([0, 0], [0, 0], [0, 1], linestyle='--', color='black', alpha=0.6)

        # Etiquetas para |0⟩ y |1⟩
        ax.text(0, 0, 1.2, r"$|0\rangle$", fontsize=12, color='black')
        ax.text(0, 0, -1.4, r"$|1\rangle$", fontsize=12, color='black')

        # Ajustes generales

        ax.set_xlim([-1.2, 1.2])
        ax.set_ylim([-1.2, 1.2])
        ax.set_zlim([-1.5, 1.5])
        ax.axis('off')

    def set_aspect_equal_3d(ax):
        extents = np.array([getattr(ax, f'get_{dim}lim')() for dim in 'xyz'])
        centers = np.mean(extents, axis=1)
        max_range = np.max(extents[:,1] - extents[:,0]) / 2

        for ctr, dim in zip(centers, 'xyz'):
            getattr(ax, f'set_{dim}lim')(ctr - max_range, ctr + max_range)

    for ax in axes:
        plot_bloch_sphere(ax)
        set_aspect_equal_3d(ax)

    # Inicializar vectores y trayectorias
    vectors = [None] * n_qubits
    trayectorias = [[] for _ in range(n_qubits)]

    # Función de actualización por frame
    def update(frame):
        for i in range(n_qubits):
            ket = reducir_qubit(estados_np[frame], i, n_qubits)
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