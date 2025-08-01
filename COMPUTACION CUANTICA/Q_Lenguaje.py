#Lenguaje para Computación Cuántica

from matrices import *
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

ver = vermatrizf

#Qubits |0> y |1> en la base z
ket0 = [[1],[0]]
ket1 = [[0],[1]]

bra0 = [[1,0]]
bra1 = [[0,1]]

#Sistemas de 2 qubits
ket00 = tensorial(ket0,ket0)
ket01 = tensorial(ket0,ket1)
ket10 = tensorial(ket1,ket0)
ket11 = tensorial(ket1,ket1)

bra00 = trasponer(ket00)
bra01 = trasponer(ket01)
bra10 = trasponer(ket10)
bra11 = trasponer(ket11)

#Compuerta Reset (irreversible) pone qubit en estado |0>
Rst=[[1,1],[0,0]]

#Clifford Group
  #Matriz Identidad
I=[[1,0],[0,1]]

  #Matrices de Pauli
X=[[0,1],[1,0]]
Y=[[0,complex(0,-1)],[complex(0,1),0]]
Z=[[1,0],[0,-1]]

  #Operador de Hadamard
H=[[2**(-0.5),2**(-0.5)],[2**(-0.5),-2**(-0.5)]]

  #Rotacion pi/2 alrededor del eje z
S=[[1,0],[0,complex(0,1)]]
Sdg=[[1,0],[0,complex(0,-1)]]

 #Rotacion pi/4 alrededor del eje z
T=[[1,0],[0,math.e**complex(0,math.pi/4)]]
Tdg=[[1,0],[0,math.e**complex(0,-math.pi/4)]]

 #CNOT o Controlled NOT o XOR
Cx=[[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]

 #I-CNOT Controlled NOT Invertida Controlada por el 2do.qubit
Xc=[[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]

 #Oraculos cuánticos (Matrices asociadas a las 4 funciones boleanas f de 1 entrada)
    # f(0)=0 , f(1)=0
U00 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    # f(0)=0 , f(1)=1
U01 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

    # f(0)=1 , f(1)=0
U10 = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    # f(0)=1 , f(1)=1
U11 = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    #se construye haciendo: U11=sumar(
    #sumar(multiplicar(ket00,bra01),multiplicar(ket01,bra00)),
    #sumar(multiplicar(ket10,bra11),multiplicar(ket11,bra10)) )

 #Oraculo cuántico (Matriz asociada a la función f AND de 2 entradas)
    # f(0,0)=0, f(0,1)=0, f(1,0)=0, f(1,1)=1 ; NO balanceada
Uand2 = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]]

 #Oraculo cuántico (Matriz asociada a la función f XOR de 2 entradas)
    # f(0,0)=0, f(0,1)=1, f(1,0)=1, f(1,1)=0 ; Balanceada
Uxor2 = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1]]

 #Oraculo cuántico (Matriz asociada a la función f constante=1 de 2 entradas)
    # f(0,0)=1, f(0,1)=1, f(1,0)=1, f(1,1)=1 ; Constante (siempre=1)
Ucte2 = [[0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]]

## Funciones ##

def h(v):
    return(multiplicar(H, v))

def x(v):
    return(multiplicar(X, v))

def y(v):
    return(multiplicar(Y, v))

def z(v):
    return(multiplicar(Z, v))

def s(v):
    return(multiplicar(S, v))

def sdg(v):
    return(multiplicar(Sdg, v))

def t(v):
    return(multiplicar(T, v))

def tdg(v):
    return(multiplicar(Tdg, v))

def cx(v0, v1):
    R = multiplicar(Cx, tensorial(v0,v1))
    return(R)

def xc(v0, v1):
    R = multiplicar(Xc, tensorial(v0,v1))
    return(R)


def cxNqubit(cantqubits, control, target): # Retorna compuerta Controled Not del qubit control al qubit target
                                           # para un nqubit, q0,q1,....q(cantqubits-1)
    if (cantqubits < 2 or control >= cantqubits or target >=cantqubits or control==target): #chequea si hay errores
        return(0)
    filas=int(2**cantqubits)
    R = I                      # Matriz Identidad 2x2
    for j in range (cantqubits-1):
        R = tensorial(I, R)    #  Matriz Identidad 2^cantqubits x 2^cantqubits
    for f in range (filas):
        b = format(f,"b").zfill(cantqubits) # arma código binario ('000...' a '111...'
        if(b[control]=="1"):   # si qubit control == 1
            valort = eval(b[target]) ^ 1 # b[target] XOR 1
            columna = 0
            for j in range(cantqubits):
                if j != target:
                    columna += eval(b[j]) * 2**(cantqubits-1-j)
            columna += valort * (2**(cantqubits-1-target)) #columna con un 1 en la fila
            for c in range (filas):
                if c==columna:
                    R[f][c]=1
                else:
                    R[f][c]=0
    return(R)


def proba(M):   #Matriz de probabilidades
    R=[]
    for i in range (len(M)):
        R.append([])
        for j in range (len(M[0])):
            modulo = M[i][j]*M[i][j].conjugate()
            R[i].append(modulo.real)
    return(R)

def rotar(radianes):  #Matriz de rotacion de radianes alrededor del eje z (Phase gate P)
    R=[[1,0],[0,math.e**complex(0,radianes)]]
    return(R)

def p(radianes, vector):  #Phase shift (rotar vector alrededor de Z)
	return(multiplicar(rotar(radianes),vector))

def medir(qubit):   #Operador de medición de un n-qubit
    posicion=[]
    probas = proba(trasponer(qubit))[0] #array de probas (peso) de cada estado
    for i in range (len(qubit)):
        posicion.append(i)      #array con posiciones numericas de cada estado (0 a n-1)
    m = random.choices(posicion, weights=probas)[0] #elige estado random según peso
    q=[]
    for i in range (len(qubit)):        #rearma qubit del estado medido
        q.append([])
        if i == m:
            q[i].append(1)
        else:
            q[i].append(0)
    return(q)

def medirEnsamble(nqubit, repeticiones): #Mide repeticiones veces para estadística
    mediciones=[]  #Vector para sumar los resultados de cada medición
    for i in range (len(nqubit)):  #inicializa en 0
        mediciones.append([])
        mediciones[i].append(0)
    for i in range (repeticiones):  #Mide y suma el resultado a mediciones
        mediciones = sumar(mediciones, medir(nqubit))
    return(mediciones)      #Retorna vector suma de mediciones para cada estado


def fase(vector):   #Calcula las fases de cada componente de un vector de estado
    if (len(vector[0]) > 1): #si no es vector columna retorna 0 y termina
        return(0)
    f=[]
    for i in range (len(vector)):   #rearma qubit del estado medido
        f.append([])
        f[i].append(math.degrees(math.atan2(vector[i][0].imag,vector[i][0].real)))
    return(f)


def normalizar(vector):   #Normaliza amplitudes de un vector para convertirlo en un qubit
    if (len(vector[0]) > 1): #si no es vector columna retorna 0 y termina
        return(0)
    q = []
    p = proba(vector)
    norma = 0
    for i in range (len(p)):
        norma += p[i][0]
    norma = math.sqrt(norma)    #raiz cuadrada de la suma de las probas de c/estado
    if(norma > 0):              #si la norma > 0
        for i in range (len(vector)):   #rearma qubit correspondiente al vector de entrada
            q.append([])
            q[i].append(vector[i][0]/norma)
    else:                       #si la norma==0 no puede normalizar vector
        q = 0                   #y retorna 0 (error)
    return(q)


def colapsar(vector, qubitNro, valor):   #Retorna qubit resultante después de medir qubitNro con valor 0 o 1
    if (len(vector[0]) != 1): #si no es vector columna retorna 0 y termina
        return(0)
    digitos=int(math.log(len(vector),2))
    q=[]
    for i in range (len(vector)):   # para cada elemento del vector de entrada
        ib=format(i,"b").zfill(digitos) # arma código binario ('000...' a '111...')
        q.append([])
        if(eval(ib[qubitNro])==valor):  # pasa estados que correspondan
            q[i].append(vector[i][0])   # con su valor de amplitud
        else:
            q[i].append(0)              # y el resto los deja con amplitud 0
    return(normalizar(q))           # Retorna qubit resultante normalizado


def reset(vector, qubitNro):    #Retorna qubit resultante después de resetear qubitNro a estado }0>
    cantqubits=int(math.log(len(vector),2)) #cantidad de qubits del vector
    if ((len(vector[0]) != 1) or (qubitNro >= cantqubits)): #si no es vector columna o qubitNro fuera de rango retorna 0 y termina
        return(0)
    Rn = Rst                    #matriz para resetear un 1qubit a estado |0>
    for i in range (cantqubits):  #arma la matriz para resetear el qubitNro del vector
        if(i<qubitNro):
            Rn = tensorial(I,Rn)
        elif(i>qubitNro):
            Rn = tensorial(Rn,I)
    q = normalizar(multiplicar(Rn, vector)) #resetea el qubitNro del vector y normaliza
    return(q)                               #retorna el nuevo vector con el qubitNro en estado |0>


def graficar(qubit,titulo="Vector de estado del qubit"):   #Grafica qubit (amplitudes vector de estado y probas)
    if (len(qubit[0]) > 1): #si no es vector columna retorna 0 y termina
        return(0)
    digitos=int(math.log(len(qubit),2))
    eje_x = []
    eje_y1 = trasponer(qubit)[0]
    eje_y2 = trasponer(proba(qubit))[0]
    eje_y3 = trasponer(fase(qubit))[0]
    for i in range (len(qubit)):
        ib=format(i,"b").zfill(digitos)
        eje_x.append(ib)
        eje_y1[i]=((eje_y1[i]*eje_y1[i].conjugate())**0.5).real

    fig, (w1, w2, w3) = plt.subplots(3,1)  #Figura con 3 gráficos en 3 filas 1 columna
    fig.suptitle(titulo)

    #fila 1 columna 1 Ventana 1
    p1 = w1.bar(eje_x, eje_y1, label="Amplitudes", color="blue")
    w1.legend(loc='best')
    w1.set_ylim(0, 1.1)
    w1.bar_label(p1, label_type='center')
    
    #fila 2 columna 1 Ventana 2
    p2 = w2.bar(eje_x, eje_y2, label="Probabilidades", color="orange")
    w2.legend(loc='best')
    w2.set_ylim(0, 1.1)
    w2.bar_label(p2, label_type='center')

    #fila 1 columna 3 Ventana 3
    p3 = w3.bar(eje_x, eje_y3, label="Fases", color="red")
    w3.legend(loc='best')
    w3.set_ylim(-190, 190)
    w3.axhline(0, color='grey', linewidth=1)
    w3.bar_label(p3, label_type='center')

    plt.show()
    return

def deutsch(Uf, q1=ket0, q2=ket1):  #Algoritmo de DEUTSCH (debe ser q12=ket01)
    q12=tensorial(q1, q2)   #Uf = oraculo booleano U00, U01, U10 o U11
    H2=tensorial(H, H)
    HI=tensorial(H, I)
    vermatrizf(multiplicar(HI, multiplicar(Uf, multiplicar(H2,q12))))
    return

def djozsa(Ufn):  #Algoritmo de DEUTSCH-JOSZA de n entradas (n + ket1 auxiliar)
                #Ufn = matriz 2^(n+1)*2^(n+1) (oraculo función booleana de n entradas)
    if (len(Ufn)==len(Ufn[0])):
        q = ket1
        Hn = H
        n = int(math.log2(len(Ufn)))-1
        for i in range(n):   # CUIDADO! se trabaja con matrices de 2^(n+1)*2^(n+1)
            q = tensorial(ket0, q)
            HmI = tensorial(Hn, I)  # HmI = Hn ant x I
            Hn = tensorial(H, Hn)   # H x Hn ant
        vermatrizf(multiplicar(HmI, multiplicar(Ufn, multiplicar(Hn,q))))
        return
    else:
        return(0)

def groverUs(n_qubits):         #Arma la compuerta Us = 2|s><s|-I (Difusor de Grover)
    if(n_qubits < 2):           #para un sistema de n_qubits (N=2**n_qubits estados)
        return(0)               #mínimo 2 qubits (sino retorna 0)
    In = I                      #Matriz Identidad
    supn = h(ket0)              #Superposición |+>
    for n in range (n_qubits - 1):
        In = tensorial(I, In)           #Matriz Identidad N x N
        supn = tensorial(supn, h(ket0)) #Estado de superposición |+> de n_qubits
    Usn = sumar(escalar(multiplicar(supn,conjugar(trasponer(supn))),2),escalar(In, -1))
    return(Usn)

# --- Función para construir un ket desde una cadena binaria ---
def construir_ket(binario):
    """
    Construye un ket a partir de una cadena binaria.
    binario: cadena de caracteres '0' y '1' representando el estado del qubit
    """
    mapa = {'0': ket0, '1': ket1}
    estado = mapa[binario[0]]
    for bit in binario[1:]:
        estado = tensorial(estado, mapa[bit])
    return estado

# --- Construcción del oráculo Uw ---
def construir_oraculo(estados_marcados, identidad):
    """
    Construye el operador Uw = I - 2 * sum(|w_i><w_i|) para múltiples soluciones.
    estados_marcados: lista de vectores columna (kets) que representan los estados marcados
    identidad: matriz identidad del espacio (por ejemplo, I3 para 3 qubits)
    """
    estado0 = estados_marcados[0]
    W_total = multiplicar(estado0, trasponer(estado0))  # primer proyector
    W_total = escalar(W_total, 0)  # matriz cero con misma forma

    for estado in estados_marcados:
        proyector = multiplicar(estado, trasponer(estado))
        W_total = sumar(W_total, proyector)

    Uw = sumar(identidad, escalar(W_total, -2))
    return Uw

def reducir_qubit(estado, qubit_index, n_qubits):
    rho = np.outer(estado, np.conj(estado))
    rho_reducido = np.zeros((2, 2), dtype=complex)
    dim = 2 ** n_qubits

    for i in range(dim):
        for j in range(dim):
            bin_i = format(i, f"0{n_qubits}b")
            bin_j = format(j, f"0{n_qubits}b")
            if bin_i[:qubit_index] + bin_i[qubit_index+1:] == bin_j[:qubit_index] + bin_j[qubit_index+1:]:
                b_i = int(bin_i[qubit_index])
                b_j = int(bin_j[qubit_index])
                rho_reducido[b_i, b_j] += rho[i, j]

    vals, vecs = np.linalg.eigh(rho_reducido)
    idx = np.argmax(vals)
    ket_reducido = vecs[:, idx]
    return [[amp] for amp in ket_reducido]

def ket_to_bloch_vector(ket):
    a, b = ket[0], ket[1]
    x = 2 * np.real(np.conj(a) * b)
    y = 2 * np.imag(np.conj(b) * a)
    z = np.abs(a)**2 - np.abs(b)**2
    return [x, y, z]

def bloch_animacion(n_qubits, estados_np):
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

def medir_parcial(estado, qubits_a_medir):
    # Simula medición de qubits específicos en un estado de n qubits
    # Devuelve: resultado medido (como string), estado proyectado y normalizado
    resultados = []
    n = int(math.log2(len(estado)))  # número de qubits
    for i in range(len(estado)):
        binario = format(i, f'0{n}b')
        resultado = ''.join([binario[q] for q in qubits_a_medir])
        resultados.append(resultado)

    # Agrupar amplitudes por resultado
    resultado_dict = {}
    for i, r in enumerate(resultados):
        if r not in resultado_dict:
            resultado_dict[r] = []
        resultado_dict[r].append(i)

    # Calcular probabilidades
    probas = {}
    for r, indices in resultado_dict.items():
        probas[r] = sum(abs(estado[i][0])**2 for i in indices)

    # Elegir resultado según probabilidad
    elegido = random.choices(list(probas.keys()), weights=list(probas.values()))[0]

    # Proyectar y normalizar
    nuevo_estado = [[0] for _ in range(len(estado))]
    for i in resultado_dict[elegido]:
        nuevo_estado[i][0] = estado[i][0]
    nuevo_estado = normalizar(nuevo_estado)

    return elegido, nuevo_estado