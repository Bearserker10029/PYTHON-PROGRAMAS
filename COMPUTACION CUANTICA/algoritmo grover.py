# Algoritmo de Grover para encontrar un elemento en una lista no ordenada
from Q_Lenguaje import *
from math import pi, sqrt, floor
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

# --- Ejecutar ambas visualizaciones en paralelo ---
if __name__ == "__main__":
    p1 = Process(target=graficar, args=(estado_final,))
    p2 = Process(target=bloch_animacion, args=(n_qubits, estados_np,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()