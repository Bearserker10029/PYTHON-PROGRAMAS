from Q_Lenguaje import *
import math
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process

np.random.seed()

# Generar α y β aleatorios normalizados (estado puro)
theta = np.random.uniform(0, np.pi)       # Ángulo polar
phi_angle = np.random.uniform(0, 2*np.pi) # Ángulo azimutal

alpha = np.cos(theta/2)
beta = np.sin(theta/2) * np.exp(1j * phi_angle)

psi=sumar(escalar(ket0, alpha), escalar(ket1, beta))  # Estado inicial |0> + |1>
# ver (psi)

phi=escalar(sumar(ket00, ket11),1/math.sqrt(2))  # Estado inicial |00> + |11>
# ver(phi)

psi0=tensorial(psi,phi)
# ver(psi0)

psi1=multiplicar(cxNqubit(3, 0, 1), psi0)  # Aplicar la compuerta CNOT
# ver(psi1)

H1=tensorial(H,tensorial(I, I))  # Aplicar la compuerta Hadamard al primer qubit
# ver(H1)

psi2=multiplicar(H1, psi1)  # Aplicar Hadamard al primer qubit
# ver(psi2)

def correccion_condicional(estado, resultado):
    if resultado == '01':
        X2=tensorial(I,tensorial(I,X))
        return multiplicar(X2, estado)  # Aplicar X al tercer qubit
    elif resultado == '10':
        Z2=tensorial(I,tensorial(I,Z))
        return multiplicar(Z2, estado)  # Aplicar Z al tercer qubit
    elif resultado == '11':
        X2=tensorial(I,tensorial(I,X))
        Z2=tensorial(I,tensorial(I,Z))
        return multiplicar(Z2, multiplicar(X2, estado))  # Aplicar X y Z al tercer qubit
    else:
        return estado

resultado, estado_proyectado = medir_parcial(psi2, [0, 1])
estado_corregido = correccion_condicional(estado_proyectado, resultado)

estados_np = [psi0, psi1, psi2, estado_proyectado, estado_corregido]

# Reducir el estado al qubit teletransportado
qubit_teletransportado = reducir_qubit(estado_corregido, 2,3) # Reducir al qubit teletransportado
print(f"Resultado de medición: {resultado}")

# --- Ejecutar ambas visualizaciones en paralelo ---
if __name__ == "__main__":
    n_qubits = 3
    p1 = Process(target=graficar, args=(psi,"Estado original |ψ⟩"))
    p2 = Process(target=graficar, args=(qubit_teletransportado,"Qubit teletransportado"))
    p3 = Process(target=bloch_animacion, args=(n_qubits, estados_np,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    # Calcular la fidelidad del qubit teletransportado con respecto al estado original
    fidelidad = abs(np.vdot(psi, qubit_teletransportado))**2
    print(f"Fidelidad: {fidelidad:.4f}")
