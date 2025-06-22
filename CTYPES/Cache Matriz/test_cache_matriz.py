import ctypes
import numpy as np
import time
import matplotlib.pyplot as plt
import statistics

if __name__ == '__main__':
    lib = ctypes.CDLL('./lib_cache.so')
    
    # Updated function signatures to match the corrected C code
    # The C functions expect 2D arrays, so we use contiguous 2D arrays
    #Completar código de ctypes para test_cache de c con sus parametros
    PPDOUBLE = np.ctypeslib.ndpointer(dtype=np.float64)
    lib.test_cache.argtypes = [PPDOUBLE,PPDOUBLE,PPDOUBLE,PPDOUBLE,ctypes.c_int, ctypes.c_int ]

    #Completar código de ctypes para test_cache2 de c con sus parametros
    
    lib.test_cache2.argtypes = [PPDOUBLE,PPDOUBLE,PPDOUBLE,PPDOUBLE,ctypes.c_int, ctypes.c_int ]


    # Test different matrix sizes - using square matrices for simplicity
    Sizes = [64, 128, 256, 512, 1024]
    iteraciones = 30
    lista1 = []
    lista2 = []
    
    for N in Sizes:
        M = N  # Using square matrices
        print(f"Testing with N={N}, M={M}")
        #Crear los arreglos de 2 dimensiones para cada test en el bucle "iteration" de la funcion test_cache
        # Create 2D arrays for each test
        a1= np.random.rand(N,M).astype(np.float64)
        print(a1)
        b1= np.random.rand(N,M).astype(np.float64)
        print(b1)
        c1= np.random.rand(N,M).astype(np.float64)
        print(c1)
        d1= np.random.rand(N,M).astype(np.float64)
        print(d1)
        
        #Crear los arreglos de 2 dimensiones para cada test en el bucle "iteration" de la funcion test_cache2
        a2= np.random.rand(N,M).astype(np.float64)
        print(a2)
        b2= np.random.rand(N,M).astype(np.float64)
        print(b2)
        c2= np.random.rand(N,M).astype(np.float64)
        print(c2)
        d2= np.random.rand(N,M).astype(np.float64)
        print(d2)
        
        #lista de tiempos de prueba de test_cache
        lista_in_1 = []
        #lista de tiempos de prueba de test_cache2
        lista_in_2 = []
        
        for iteration in range(iteraciones):
            #mide el tiempo de ejecución de test_cache y lo registra en lista_in_1
            
            inicio1= time.perf_counter()
            lib.test_cache(a1,b1,c1,d1,N,M)
            fin1= time.perf_counter()
            lista_in_1.append(fin1-inicio1)
            
            
            #mide el tiempo de ejecución de test_cache y lo registra en lista_in_1
            inicio2= time.perf_counter()
            lib.test_cache2(a2,b2,c2,d2,N,M)
            fin2= time.perf_counter()
            lista_in_2.append(fin2-inicio2)
        
        lista1.append(statistics.median(lista_in_1))
        lista2.append(statistics.median(lista_in_2))
        print(f"  Function 1 median time: {lista1[-1]:.6f}s")
        print(f"  Function 2 median time: {lista2[-1]:.6f}s")

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(Sizes, lista1, 'r-o', label='test_cache (combined loops)')
    plt.plot(Sizes, lista2, 'g-s', label='test_cache2 (split loops)')
    plt.grid(True)
    plt.legend()
    plt.xlabel("Matrix Size (N x N)")
    plt.ylabel("Time (seconds)")
    plt.title("Cache Performance Comparison")
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    
    # Print summary
    print("\nPerformance Summary:")
    for i, size in enumerate(Sizes):
        ratio = lista2[i] / lista1[i]
        print(f"Size {size}x{size}: Function1={lista1[i]:.6f}s, Function2={lista2[i]:.6f}s, Ratio={ratio:.3f}")