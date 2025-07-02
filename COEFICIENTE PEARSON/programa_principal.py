import numpy as np
import ctypes
import math
import time
import statistics
import matplotlib.pyplot as plt

def calcular_Pearson(arreglo_x,arreglo_y,N):
    suma_x = 0
    sx = 0
    for i in range(N):
        suma_x = arreglo_x[i]+suma_x
    prom_x = suma_x/N

    for i in range(N):
        sx = (arreglo_x[i]-prom_x)**2+sx
    sx = math.sqrt(sx)

    suma_y = 0
    sy = 0
    for i in range(N):
        suma_y = arreglo_y[i]+suma_y
    prom_y = suma_y/N

    for i in range(N):
        sy = (arreglo_y[i]-prom_y)**2+sy
    sy = math.sqrt(sy)

    sxy = 0
    for i in range(N):
        sxy = (arreglo_x[i]-prom_x)*(arreglo_y[i]-prom_y) +sxy

    return sxy/(sx*sy)

if __name__ == '__main__':

    tam = [2**8, 2**10, 2**12, 2**16, 2**18, 2**20]
    lib = ctypes.CDLL('./lib_coef.so')
    lib.calcular_Pearson_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.int16),np.ctypeslib.ndpointer(dtype=np.int16), ctypes.c_int]
    lib.calcular_Pearson_c.restype = ctypes.c_double

    lib_Os = ctypes.CDLL('./lib_coef_Os.so')
    lib_Os.calcular_Pearson_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.int16),np.ctypeslib.ndpointer(dtype=np.int16), ctypes.c_int]
    lib_Os.calcular_Pearson_c.restype = ctypes.c_double
    lista_tiempo = []
    lista_tiempoc = []
    lista_tiempocOs = []
    iteraciones = 15
    for N in tam:
        x = np.random.randint(0,20,N,dtype=np.int16)
        y = np.random.randint(0,20,N,dtype=np.int16)
        lista_iteraciones = []
        lista_iteracionesc = []
        lista_iteracionescOs = []
        for _ in range(iteraciones):
            t1 = time.perf_counter()
            rxy = calcular_Pearson(x,y,N)
            t1_out = time.perf_counter()
            t2 = time.perf_counter()
            rxy_c = lib.calcular_Pearson_c(x,y,N)
            t2_out = time.perf_counter()
            t3 = time.perf_counter()
            rxy_c_Os = lib_Os.calcular_Pearson_c(x,y,N)
            t3_out = time.perf_counter()
            lista_iteraciones.append(t1_out-t1)
            lista_iteracionesc.append(t2_out-t2)
            lista_iteracionescOs.append(t3_out-t3)
        lista_tiempo.append(statistics.median(lista_iteraciones))
        lista_tiempoc.append(statistics.median(lista_iteracionesc))
        lista_tiempocOs.append(statistics.median(lista_iteracionescOs))

#    plt.plot(tam,lista_tiempo, 'r')
#    plt.plot(tam,lista_tiempoc, 'g')
#    plt.plot(tam,lista_tiempocOs, 'b')
#    plt.grid()
#    plt.legend(['Python','C', 'C - Os'])
#    plt.show()

    plt.plot(tam,lista_tiempoc, 'g')
    plt.plot(tam,lista_tiempocOs, 'b')
    plt.grid()
    plt.legend(['C', 'C - Os'])
    plt.show()