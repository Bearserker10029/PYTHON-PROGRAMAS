import numpy as np
import ctypes
import math
import time
import statistics
import matplotlib.pyplot as plt
import math
import numpy as np

def ordena(N,arreglo, arreglosalida):
    for i in range(N//4):
        for j in range(4):
            if (j==3):
                numcopia=arreglo[i*4+j]
                arreglo_salida[i*4+j]=arreglo[i*4]
                arreglo_salida[i*4]=numcopia
            else:
                arreglo_salida[i*4+j]=arreglo[i*4+j]
    return arreglo_salida


if __name__== "__main__":
    N=16
    
    arreglo=np.random.randint(100,size=(N)).astype(np.int64)
    arreglo_salida=np.zeros_like(arreglo)
    arreglo_salidac=np.zeros_like(arreglo)
    ordena(N,arreglo,arreglo_salida)
    print("arreglo entrada ",arreglo)
    print("arreglo salida ",arreglo_salida)
    
    lib = ctypes.CDLL('./ordena.so')
    lib.ordenac.argtypes = [ctypes.c_int32, np.ctypeslib.ndpointer(dtype=np.int64),np.ctypeslib.ndpointer(dtype=np.int64)]
    lib.ordenac.restypes = [np.ctypeslib.ndpointer(dtype=np.int64)]
    lib.ordenac(N, arreglo, arreglo_salidac)
    print("arreglo en c",arreglo_salidac)
    
    lista_tiempo=[]
    lista_tiempoc = []

    tam=[2**8, 2**10, 2**12, 2**16, 2**18, 2**20]
    iteraciones=15
    for N in tam:
        arreglo=np.random.randint(100,size=(N)).astype(np.int64)
        arreglo_salida=np.zeros_like(arreglo)
        arreglo_salidac=np.zeros_like(arreglo)
        lista_iteraciones = []
        lista_iteracionesc = []
        lista_iteracionescOs = []
        for _ in range(iteraciones):
            t1 = time.perf_counter()
            ordena(N,arreglo,arreglo_salida)
            t1_out = time.perf_counter()
            
            t2 = time.perf_counter()

            lib.ordenac(N, arreglo, arreglo_salidac)
            t2_out = time.perf_counter()

            lista_iteraciones.append(t1_out-t1)
            lista_iteracionesc.append(t2_out-t2)
        lista_tiempo.append(statistics.median(lista_iteraciones))
        lista_tiempoc.append(statistics.median(lista_iteracionesc))

    plt.plot(tam,lista_tiempo, 'g')
    plt.plot(tam,lista_tiempoc, 'b')
    plt.grid()
    plt.legend(['Python','C'])
    plt.show()