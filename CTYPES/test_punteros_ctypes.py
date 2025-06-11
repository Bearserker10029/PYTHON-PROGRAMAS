import ctypes
import numpy as np
import time

def modifica_arreglo(arreglo_in,arreglo_out,N):
    for i in range(N):
        arreglo_out[i] = arreglo_in[i]*10

if __name__ == '__main__':

    
    N = 1024*1024
    
    arreglo = np.random.randint(10,20,N,dtype = np.int8)
    arreglo_salida = np.zeros_like(arreglo)
    arreglo_salida2 = np.zeros_like(arreglo)

    lib = ctypes.CDLL('./lib_arreglo.so')
    lib.modifica_arreglo_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.int8),np.ctypeslib.ndpointer(dtype=np.int8),ctypes.c_int32]

    
    t1 = time.perf_counter()
    modifica_arreglo(arreglo,arreglo_salida,N)
    t2 = time.perf_counter()
    print("Enteros Python",t2-t1)
    #print(arreglo_salida)
    t1 = time.perf_counter()
    lib.modifica_arreglo_c(arreglo,arreglo_salida2,N)
    #print(arreglo_salida2)
    t2 = time.perf_counter()
    print("Enteros C",t2-t1)

    arreglo_float = np.random.rand(N).astype(np.float32)
    #print(type(arreglo_float[0]))
    arreglo_salida_float = np.zeros_like(arreglo_float)
    arreglo_salida_float2 = np.zeros_like(arreglo_float)
    lib.modifica_arreglo_c_float.argtypes = [np.ctypeslib.ndpointer(dtype=np.float32),np.ctypeslib.ndpointer(dtype=np.float32),ctypes.c_int32]

    t1 = time.perf_counter()
    modifica_arreglo(arreglo_float,arreglo_salida_float,N)
    t2 = time.perf_counter()
    print("Flotantes Python",t2-t1)
    #print(arreglo_salida_float)
    t1 = time.perf_counter()
    lib.modifica_arreglo_c_float(arreglo_float,arreglo_salida_float2,N)
    t2 = time.perf_counter()
    print("Flotantes C",t2-t1)
    #print(arreglo_salida_float2)


    